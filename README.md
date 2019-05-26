# Logs Analysis Project

This project answers the three questions below based on psql db created from the `newsdata.sql` file.
(See Questions To Answer Section)

# Requirements To Run Code

These need to be installed on your machine:

- Vagrant
- Vagrant Box
- Python 3

# To Run The Project

1. Clone this directory and cd into it

```
git clone
cd logs-analysis
```

2. Download dataset from here: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
   Unzip it, and put the newsdata.sql file into the logs-analysis folder you just cloned.

3. Launch vagrant, ssh to it, and cd into /vagrant directory, and load data

```
vagrant up
vagrant ssh

// (once in vagrant)
cd /vagrant

// load tables in vagrant
psql -d news -f newsdata.sql
```

4. Run code to produce output to questions, output will be created in output.txt file in the same directory once code is ran.

```
python analysis.py
```

5. Review `report.txt` for the answers to questions.

# Views used in the code (to answer question 3)

```
create view totals as
    select to_char(time, 'Mon DD, YYYY') as day, count(status) as total
        from log
        group by day;

create view failed as
    select to_char(time, 'Mon DD, YYYY') as day, count(status) as errors
        from log
        where status != '200 OK'
        group by day;
```

Ps: views are deleted before the execution statement of creation of these views, in order not to produce errors when person reruns the analysis.py script.

# Questions To Answer

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

Example:

"Princess Shellfish Marries Prince Handsome" — 1201 views
"Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
"Political Scandal Ends In Political Scandal" — 553 views

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

Example:

Ursula La Multa — 2304 views
Rudolf von Treppenwitz — 1985 views
Markoff Chaney — 1723 views
Anonymous Contributor — 1023 views

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

Example:

July 29, 2016 — 2.5% errors
