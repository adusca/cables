import json
import psycopg2
import re

from collections import defaultdict


class DocumentMatrix:

    def __init__(self, size, filename):
        self.word_to_index = {}
        self.index_to_word = []
        self.cur_index = 0
        self.size = size
        self.filename = filename
        self.matrix = {}

    def pretty_print(self, document_vector):
        for key in document_vector:
            print self.index_to_word[key], ":", document_vector[key]

    def process_all_documents(self):
        con = psycopg2.connect("dbname='base' user='alice'")
        print "Conectado a db"
        cur = con.cursor()
        cur.execute("SELECT * FROM cable")
        remove_chars = re.compile(r'[.?!,":;()|0-9]')

        for i in range(self.size):  # O total de documentos eh 251288
            document = cur.fetchone()[-1]
            document_array = document.split()
            document_array = [" ".join(remove_chars.sub(" ", word).split())
                              for word in document_array]
            document_word_count = defaultdict(int)
            for word in document_array:
                if word not in self.word_to_index:
                    self.word_to_index[word] = self.cur_index
                    self.cur_index += 1
                    self.index_to_word.append(word)
                document_word_count[self.word_to_index[word]] += 1

            self.matrix[i] = document_word_count

        # Fechando a conexao
        con.close()
        with open(self.filename, 'w') as f:
            json.dump(self.matrix, f)
        with open("word_list.json", "w") as f:
            json.dump(self.index_to_word, f)
        return self.matrix
