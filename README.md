LOG ANALYSIS:

->Description:
	->Log Analysis project deals with a huge data records in the form of tables like authors, articles and log.
	  The data present in these tables are used in finding the following results:
		i)	What are the most popular three articles of all time?
		ii)	Who are the most popular article authors of all time?
		iii)On which days did more than 1% of the requests lead to errors?

->The Required Software Installations:
	->python
	->vagrant
	->virtualbox

->Now open command prompt/git bash from the folder where you have the python file. Then add a virtual environment like ubuntu/trusty64 to the box:
	-> vagrant box add ubuntu/trusty64
	-> vagrant init ubuntu/trusty64

->Now setup the vagrant and configure :
	->vagrant up
	->vagrant ssh

->Now vagrant starts running successfully.

->Now change to vagrant folder.

->And install postgres, psycopg2 and pip using: 
	->sudo apt-get install python-postgres
	->sudo apt-get install python-psycopg2
	->sudo apt-get install python-pip

->Download the newsdata.sql file containing database and copy that file in vagrant folder.

->Create roles 'Vagrant' and 'postgres'.
	->sudo -i -u postgres	
	->sudo -i -u vagrant

->Create two databases 'vagrant' and 'news' with vagrant as the p:
	->create database vagrant
	->create database news

->Copy the data from newsdata.sql file to the news database:
	->psql -d news -f newsdata.sql

->Run the python file "newsdataa.py" from vagrant.
