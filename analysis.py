#!/usr/bin/env python3

import psycopg2
DBNAME = "news"

# Connect to DB and initialize cursor
db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# Question 1: What are the most popular three articles of all time?
c.execute(
    """
        select articles.title, count(log.path) as times
            from articles
            inner join log
                on '/article/' || articles.slug = log.path
            where log.status = '200 OK'
            group by articles.title
            order by times desc
            limit 3;
    """
)

articles = c.fetchall()
answer1 = '1. The 3 most popular articles by views (descending) are: \n\n'
for article in articles:
    answer1 += '\"{}\" - {} views\n'.format(article[0], article[1])


# Question 2: Who are the most popular article authors of all time?
c.execute(
    """
        select authors.name, count(log.path) as times
            from log
            inner join articles
                on '/article/' || articles.slug = log.path
            inner join authors
                on authors.id = articles.author
            group by authors.name
            order by times desc;
    """
)

authors = c.fetchall()
answer2 = '2. The most popular authors by views (descending) are: \n\n'
for author in authors:
    answer2 += '{} - {} views\n'.format(author[0], author[1])

# Question 3: On which days did more than 1% of requests lead to errors?
c.execute(
    """
        drop view if exists totals;
        drop view if exists failed;

        create view totals as
            select to_char(time, 'Mon DD, YYYY') as day, count(status) as total
                from log
                group by day;

        create view failed as
            select to_char(time, 'Mon DD, YYYY') as day,
                    count(status) as errors
                from log
                where status != '200 OK'
                group by day;

        select failed.day,
                round(
                    cast(
                        (failed.errors / totals.total :: float) * 100
                    as numeric)
                , 2)
            from failed
            inner join totals
                on failed.day = totals.day
            where (failed.errors / totals.total :: float) > 0.01;
    """
)
days = c.fetchall()
answer3 = '3. Days on which more than 1% of requests lead to errors: \n\n'
for day in days:
    answer3 += '{} - {}% errors \n'.format(day[0], day[1])


# Write results to file
spacing = "\n\n"
with open("report.txt", "w+") as f:
    f.write(answer1)
    f.write(spacing)
    f.write(answer2)
    f.write(spacing)
    f.write(answer3)
