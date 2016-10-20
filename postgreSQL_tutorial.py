#!/usr/bin/python
# -*- coding: utf-8 -*-

# psycopg2 is a Python module used to interact with PostgreSQL
import psycopg2
import psycopg2.extras
import sys

con = None

cars = (
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Citroen', 21000),
    (7, 'Hummer', 41400),
    (8, 'Volkswagen', 21600)
)

try:
    con = psycopg2.connect(database='testdb', user='alice')

    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Cars")

    rows = cur.fetchall()
    for row in rows:
        print "%s %s %s" %(row['id'], row['name'], row['price'])

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
