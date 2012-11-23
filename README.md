Stacks
======

Lovingly organized pixels.

Assumes a running MySQL database and a Python environment with virtualenv.

Recommended env vars:

	export STACKS_ROOT=/Users/johnm/Projects/stacks

Create a database and user on a local MySQL:
	
	create database stacks;
	grant all on stacks.* to 'stacksuser'@'localhost' identified by 'stacksuser';

To create the environment:

	virtualenv stacks-env
	stacks-env/bin/pip install -r requirements.txt

Activate the virtualenv, syncdb and import initial data, then start the server:

	stacks-env/bin/activate
	manage.py syncdb
	manage.py loaddata kickstarter.json
	manage.py runserver