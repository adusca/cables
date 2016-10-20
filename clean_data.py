import psycopg2
import string

query_brazil = """SELECT * FROM cable
                 WHERE (origin='Embassy Brasilia'
                        OR origin='Consulate Sao Paulo'
                        OR origin='Consulate Rio De Janeiro'
                        OR origin='Consulate Recife');"""


def run():
    # Conectando ao banco de dados
    con = psycopg2.connect("dbname='base' user='alice'")
    print "Conectado a db"
    cur = con.cursor()
    cur.execute(query_brazil)
    print "Selecionando todas as linhas originadas no Brazil"
    i = 0
    while True:
        f = raw_input("digite qualquer coisa para o prox passo: ")
        row = cur.fetchone()
        if row is None:
            break
        text = row[-1].split("SUBJECT:")[-1]
        print text
        to_remove = string.punctuation + string.digits
        table = string.maketrans(to_remove, " "*len(to_remove))
        document = row[-1].translate(table).lower()
        nxt = document.split()

run()
