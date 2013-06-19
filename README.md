Stacks
======

Lovingly organized pixels.

Assumes a running MySQL database, memcached cache, and a Python environment with virtualenv.

Recommended env vars:

	STACKS_ROOT=/Users/johnm/Projects/stacks
	STACKS_LOCAL=1
    STACKS_CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
    STACKS_CACHE_LOCATION=127.0.0.1:11211

Recommended /etc/hosts:

    127.0.0.1 local.astrostacks.com local.climbingstacks.com

Create the environment:

	virtualenv stacks-env
	stacks-env/bin/pip install -r requirements.txt

Activate the virtualenv, and run the rebuild script to sync and add fixtures to the database:

	stacks-env/bin/activate
	./rebuild.sh

Start the Django development server:

    ./manage.py runserver 0.0.0.0 8000

Visit one of the local sites:

    http://local.astrostacks.com:8000
    http://local.climbingstacks.com:8000