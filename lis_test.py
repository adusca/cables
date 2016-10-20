"""Esse script extrai os documentos do banco de dados para arquivos de texto."""
#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2

con = None

# Conectando ao banco de dados
con = psycopg2.connect("dbname='base' user='alice'")
print "Conectado a db"
cur = con.cursor()
cur.execute("SELECT * FROM cable")
print "Selecionando todas as linhas"

# Criando um arquivo por documento
for i in range(200): # O total de documentos eh 251288
    filename = "./documents/cable_%i" % i
    with open(filename,'w') as f:
        row = cur.fetchone()
        f.write(row[-1])

# Fechando a conexao
con.close()
