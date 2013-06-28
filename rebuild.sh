echo "drop database if exists stacks; create database stacks;" | mysql -ustacksuser -pstacksuser
echo "Dropped and recreated database"
./manage.py syncdb --noinput
echo "Added tables and indexes"
./manage.py loaddata kickstarter.yaml
echo "Added fixtures"

