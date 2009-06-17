mumbles github growler
======================

WHAT IS THIS:
-------------

	github growler using mumbles plugin and checker script.

REQUIRES:
---------

* mumbles : http://www.mumbles-project.org/ 
* ...

AUTHOR:
-------

	mattn

BUILD:
------

	# cd plugin
	# python setup.py bdist_egg
	# cp dist/GithubMumbles-* ~/.mumbles/plugin/.
	# cp plugin/github.png ~/.mumbles/plugin/icons/.

	# vi checker/githubcheck.py

		change USER and TOKEN in script.

	# python checker/githubcheck.py

