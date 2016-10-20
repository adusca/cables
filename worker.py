import psycopg2

con = psycopg2.connect(database='base', user='alice')
cur = con.cursor()
cur.execute('SELECT * FROM cable')
col_names = [cn[0] for cn in cur.description]

print col_names
