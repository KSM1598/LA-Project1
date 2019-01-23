#!/usr/bin/env python3
import psycopg2

tc1 = ("1. What are the most popular three articles of all time?")
q1 = ('''create view articles_view as select articles.title,
         count(*) as total_views
         from articles inner join log
         on concat('/article/', articles.slug) = log.path
         where log.status like '%200%' group by articles.title
         order by total_views desc limit 3;''')

tc2 = ("2. Who are the most popular article authors of all time?")
q2 = ('''create view authors_view as select authors.name,
         count(*) as total_views
         from authors inner join articles
         on authors.id=articles.author inner join log
         on concat('/article/', articles.slug) = log.path
         group by authors.name order by total_views desc;''')

tc3 = ("3. On which days did more than 1% of the requests lead to errors?")
q3 = ('''create view log_errors as
      select Date,Total_records,Errors,
      (Errors::float*100)/Total_records::float as Error_Percentage
      from (select time::timestamp::date as Date,
      count(status) as Total_records,
      sum(case when status like '%404%' then 1 else 0 end) as Errors
      from log group by time::timestamp::date) as result
      where (Errors::float*100)/Total_records::float > 1.0
      order by Error_Percentage desc;''')


def dbconnect(database_name="news"):
    # Connect or check database connection
    try:
        cnxn = psycopg2.connect("dbname={}".format(database_name))
        cursor = cnxn.cursor()
        print("Connection Established")
        return cnxn, cursor
    except Exception:
        print("Unable to connect to the database")


def exec_query1(q):
    cnxn, cursor = dbconnect()
    cursor.execute(q)
    qt = ("select * from articles_view;")
    cursor.execute(qt)
    cnxn.commit()
    return cursor.fetchall()
    cnxn.close()


def exec_query2(q):
    cnxn, cursor = dbconnect()
    cursor.execute(q)
    qt = ("select * from authors_view;")
    cursor.execute(qt)
    cnxn.commit()
    return cursor.fetchall()
    cnxn.close()


def exec_query3(q):
    cnxn, cursor = dbconnect()
    cursor.execute(q)
    qt = ("select * from log_errors;")
    cursor.execute(qt)
    cnxn.commit()
    return cursor.fetchall()
    cnxn.close()


def print_query(query_results):
    print(query_results[1])
    for results in enumerate(query_results[0]):
        print(
            "\t" + str(results[0]+1) + " . " + str(results[1][0]) +
            " - " + str(results[1][1]) + " views \n")


def print_error_query(error_results):
    print(error_results[1])
    for results in enumerate(error_results[0]):
        print(
            "\t" + str(results[0]+1) + " . " + str(results[1][0]) + "   " +
            str(results[1][1]) + "  " + str(results[1][2]) +
            "  " + str(results[1][3]) + "% of errors \n")

if __name__ == '__main__':
    top_3_articles = exec_query1(q1), tc1
    famous_authors = exec_query2(q2), tc2
    erronous_days = exec_query3(q3), tc3

    print_query(top_3_articles)
    print_query(famous_authors)
    print_error_query(erronous_days)
