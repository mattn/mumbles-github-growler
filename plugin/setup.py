from setuptools import setup
import sys, os
from shutil import copy

__author__ = 'mattn <mattn.jp@gmail.org>'
__doc__ = 'A simple github growler plugin for mumbles.'
__version__ = '0.1'

setup(
	name='GithubMumbles',
	version=__version__,
	description=__doc__,
	author=__author__,
	packages=['github'],
	package_dir={'github':'src'},
	package_data={'':['github.png']},
	entry_points='''
	[mumbles.plugins]
	Github = github:GithubMumbles
	'''
)

copy("dist/GithubMumbles-%s-py%d.%d.egg" %(__version__,sys.version_info[0],sys.version_info[1]), "../../")
