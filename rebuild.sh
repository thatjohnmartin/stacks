echo "drop database stacks; create database stacks;" | ./manage.py dbshell
echo "Dropped and recreated database"
./manage.py syncdb --noinput
echo "Added tables and indexes"
./manage.py loaddata kickstarter.json
echo "Added fixtures"

