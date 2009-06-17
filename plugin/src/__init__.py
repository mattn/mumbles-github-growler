from MumblesPlugin import *
import dbus
import gnomevfs
import os
import urllib

class GithubMumbles(MumblesPlugin):
  plugin_name = 'GithubMumbles'
  dbus_interface = 'com.github.DBus'
  dbus_path = '/com/github/DBus'
  icons = {'github' : 'github.png'}
  __url = None

  def __init__(self, mumbles_notify, session_bus):
    self.signal_config = {
      'Notify': self.Notify,
      'NotifyNum': self.NotifyNum
    }
    MumblesPlugin.__init__(self, mumbles_notify, session_bus)
    self.add_click_handler(self.onClick)

  def NotifyNum(self, num):
    self.__url = 'http://github.com/'
    icon = self.get_icon('github')
    title = 'Github'
    msg = str(num)+' new messages!'
    self.mumbles_notify.alert(self.plugin_name, title, msg, icon)

  def Notify(self, link, author, text):
    self.__url = link
    path = os.path.join(PLUGIN_DIR_USER, 'icons', 'github-%s' % author)
    if os.path.exists(path):
      self.icons[author] = 'github-%s' % author
      icon = self.get_icon(author)
    else:
      icon = self.get_icon('github')
    self.mumbles_notify.alert(self.plugin_name, author, text, icon)

  def onClick(self, widget, event, plugin_name):
    if event.button == 3:
      self.mumbles_notify.close(widget.window)
    else:
      self.open_url(self.__url)

  def open_url(self, url):
    mime_type = gnomevfs.get_mime_type(url)
    application = gnomevfs.mime_get_default_application(mime_type)
    os.system(application[2] + ' "' + url + '" &')

