#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import psycopg2
import sys

con = None

# Conectando ao banco de dados
con = psycopg2.connect("dbname='base' user='alice'")
cur = con.cursor()
cur.execute("SELECT * FROM cable")
col_names = [cn[0] for cn in cur.description]

# Escrevendo um csv com os dados que vamos usar
with open('export.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(col_names[0:6])
    for i in range(251288):
        row = cur.fetchone()
        writer.writerow(row[0:6])

# Fechando a conexao
con.close()

# psql base
# \d+ cable
# CREATE TABLE cable2 (id integer, date timestamp without time zone, classification character varying, origin character varying, destination text);
# INSERT INTO cable2 (id, date, classification, origin, destination) SELECT id, date, classification, origin, destination FROM cable;
# \copy (SELECT id, date, classification, origin, destination FROM cable) TO 'export.csv' CSV HEADER
