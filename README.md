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

    127.0.0.1 local.stcks.com

Create the environment:

	virtualenv env
	source env/bin/activate
	pip install -r requirements.txt

Run the rebuild script to sync and add fixtures to the database:

	./rebuild.sh

Create log and cached asset dirs and make them writeable:

    mkdir /var/log/stacks
    chgrp staff /var/log/stacks
    chmod 775 /var/log/stacks

    mkdir /var/stacks
    chgrp staff /var/stacks
    chmod 775 /var/stacks

Start the Django development server:

    ./manage.py runserver 0.0.0.0 8000

Visit the local sites:

    http://www.stcks.com:8000