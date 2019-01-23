#LOG ANALYSIS:

##Description:
	Log Analysis project deals with a huge data records in the form of tables like authors, articles and log. The data present in 		these tables are used in finding the following results:
		1.	What are the most popular three articles of all time?
		2.	Who are the most popular article authors of all time?
		3.	On which days did more than 1% of the requests lead to errors?

	Views created for the above results are:
		1.	articles_view
		2.	authors_view
		3.	log_errors

	The queries for creating the views are:
		1.	create view articles_view as select articles.title,
         		count(*) as total_views
         		from articles inner join log
         		on concat('/article/', articles.slug) = log.path
         		where log.status like '%200%' group by articles.title
         		order by total_views desc limit 3;	
		2.	create view authors_view as select authors.name, 
			count(*) as total_views 
			from authors inner join articles
			on authors.id=articles.author inner join log
			on concat('/article/', articles.slug) = log.path 
			group by authors.name order by total_views desc; 	
		3.	create view log_errors as 
			select Date,Total_records,Errors,
			(Errors::float*100)/Total_records::float as Error_Percentage
			from (select time::timestamp::date as Date,
			count(status) as Total_records,
			sum(case when status like '%404%' then 1 else 0 end) as Errors
			from log group by time::timestamp::date) as result
			where (Errors::float*100)/Total_records::float > 1.0
			order by Error_Percentage desc; 	

The Required Software Installations:
	*	python
	*	vagrant
	*	virtualbox

Now open command prompt/git bash from the folder where you have the python file. Then add a virtual environment like ubuntu/trusty64 to the box:
	* 	vagrant box add ubuntu/trusty64
	* 	vagrant init ubuntu/trusty64

Now setup the vagrant and configure :
	*	vagrant up
	*	vagrant ssh

Now vagrant starts running successfully.

Now change to vagrant folder.

And install postgres, psycopg2 and pip using: 
	*	sudo apt-get install python-postgres
	*	sudo apt-get install python-psycopg2
	*	sudo apt-get install python-pip

Download the newsdata.sql file containing database and copy that file in vagrant folder.

Create roles Vagrant and postgres:
	*	sudo -i -u postgres	
	*	sudo -i -u vagrant

Create two databases vagrant and news with vagrant as the p:
	*	create database vagrant
	*	create database news

Copy the data from newsdata.sql file to the news database:
	*	psql -d news -f newsdata.sql

Run the python file newsdataa.py from vagrant.
