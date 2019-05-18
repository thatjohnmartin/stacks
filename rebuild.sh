echo "drop database if exists stacks; create database stacks;" | mysql -ustacksuser
echo "Dropped and recreated database"
./manage.py syncdb --noinput
echo "Added tables and indexes"
./manage.py loaddata kickstarter.yaml
echo "Added fixtures"
echo "Restarting memcached"
pkill memcached
memcached &
