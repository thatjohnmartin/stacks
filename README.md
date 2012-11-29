Stacks
======

Lovingly organized pixels.

Assumes a running MySQL database and a Python environment with virtualenv.

Recommended env vars:

	export STACKS_ROOT=/Users/johnm/Projects/stacks

Create the environment:

	virtualenv stacks-env
	stacks-env/bin/pip install -r requirements.txt

Activate the virtualenv, and run the rebuild script to sync and add fixtures to the database:

	stacks-env/bin/activate
	./rebuild.sh