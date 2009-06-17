#!/usr/bin/env python
USER='YOUR-GITHUB-USER-ID'
TOKEN='YOUR-GITHUB-TOKEN-ID'

UPDATE_INTERVAL=1000 # 10 minutes
MAX_NOTIFICATIONS = 40
DEBUG = True
##################################################

import feedparser
import gobject
import rfc822
import calendar
import time
import urllib
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import os
import sys
import getopt
from BeautifulSoup import BeautifulSoup

GITHUB_DBUS_INTERFACE = 'com.github.DBus'
GITHUB_DBUS_PATH = '/com/github/DBus'

class Usage(Exception):
  def __init__(self, msg=None):
    app = sys.argv[0]
    if msg != 'help':
        self.msg = app+': Invalid options. Try --help for usage details.'
    else:
      self.msg = app+": DBus notifications on new github messages.\n"

class GithubCheck(dbus.service.Object):
  def __init__(self, public_only=False):
    self._public_only = public_only

    session_bus = dbus.SessionBus()
    bus_name = dbus.service.BusName(GITHUB_DBUS_INTERFACE, bus=session_bus)
    dbus.service.Object.__init__(self, bus_name, GITHUB_DBUS_PATH)

    self.interval = UPDATE_INTERVAL
    self.notifyLimit = MAX_NOTIFICATIONS
    self.debug = DEBUG

    self.lastCheck = None

    self.minInterval = 60000 # 1 minute min refresh interval
    if self.interval < self.minInterval:
      print "Warning: Cannot check github more often than once a minute! Using default of 1 minute."
      self.interval = self.minInterval
    self._check()

  @dbus.service.signal(dbus_interface=GITHUB_DBUS_INTERFACE, signature='sss')
  def Notify(self, link, author, text):
    pass

  @dbus.service.signal(dbus_interface=GITHUB_DBUS_INTERFACE, signature='i')
  def NotifyNum(self, num):
    pass

  def unescape(self, s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&apos;", "'")
    s = s.replace("&quot;", '"')
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s

  def _check(self):
    if self.debug:
      if self.lastCheck:
        print "checking feed (newer than %s):" %(self.lastCheck)
      else:
        print "checking feed:"

    try:
      items = feedparser.parse("http://github.com/%s.private.atom/?token=%s" % (USER, TOKEN))['entries']
    except Exception, e:
      items = []

    if self.lastCheck:
      lastCheck = calendar.timegm(time.localtime(calendar.timegm(rfc822.parsedate(self.lastCheck))))
      for item in items:
        if calendar.timegm(item.published_parsed) < lastCheck:
          items.remove(item)

    self.lastCheck = rfc822.formatdate()

    num_notifications = len(items)

    if num_notifications > MAX_NOTIFICATIONS:
      if self.debug:
        print "%s new entries\n" %(num_notifications)
      self.NotifyNum(num_notifications)
    elif num_notifications < 0:
      if self.debug:
        print "no new entries\n"
    else:
      for item in items:
        path = os.path.join(os.path.expanduser('~'), '.mumbles', 'plugins', 'icons', 'github-%s' % item['author'])
        if not os.path.exists(path):
          html = urllib.urlopen('http://github.com/%s' % item['author']).read()
          soup = BeautifulSoup(html)
          img = soup.findAll('div', {'class':'identity'})[0].find('img')['src']
          urllib.urlretrieve(img, path)
        body = BeautifulSoup(item['subtitle']).findAll(text=True)
        text = ''
        for b in body:
          text = text + b.replace("\n", " ").strip()
        self.Notify(item['link'], item['author'], text)
    gobject.timeout_add(self.interval,self._check)

if __name__ == '__main__':

  DBusGMainLoop(set_as_default=True)

  public_only = False
  try:
    try:
      opts, args = getopt.getopt(
        sys.argv[1:], "hp", ["help"])
    except getopt.GetoptError:
      raise Usage()

    for o, a in opts:
      if o in ("-h", "--help"):
        raise Usage('help')
      else:
        raise Usage()
  except Usage, err:
    print >> sys.stderr, err.msg
    sys.exit(2)

  t = GithubCheck(public_only)
  try:
    loop = gobject.MainLoop()
    loop.run()
  except KeyboardInterrupt:
    print "githubcheck shut down..."
  except Exception, ex:
    print "Exception in githubcheck: %s" %(ex)

