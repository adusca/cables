import psycopg2
import gensim
import logging
import json
import os

from flask import Flask, request, jsonify, redirect, abort, session, render_template

with open("corpus2db_brazil", "r") as f:
    corpus2db = json.load(f)
    corpus2db = {int(key): val for (key, val) in corpus2db.iteritems()}

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


d = gensim.corpora.Dictionary()

dictionary = d.load("binary_dict_brazil")
corpus = gensim.corpora.MmCorpus('corpus_lsi_brazil.mm')

tfidf = gensim.models.TfidfModel.load("tfidf_model_brazil")

lsi = gensim.models.LsiModel.load("lsi_model_brazil")

index = gensim.similarities.MatrixSimilarity(corpus, num_features=100)


def transform(query):
    vec_query = dictionary.doc2bow(query.lower().split())
    query_tfidf = tfidf[vec_query]
    return lsi[query_tfidf]


con = psycopg2.connect("dbname='base' user='alice'")
cur = con.cursor()

app = Flask(__name__)
app.secret_key = os.environ.get("CABLE_KEY")
app.config["SESSION_TYPE"] = "filesystem"
PORT = 8080
DOMAIN = 'localhost:%d' % PORT


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/busca", methods=["POST"])
def search():
    query = request.form['query']

    query_lsi = transform(query)
    sims = index[query_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])[:10]
    results = []
    for doc in sims:
        cur.execute("SELECT * FROM cable WHERE id = %i;" % corpus2db[doc[0]])
        results.append(cur.fetchall()[0][-1][:200])
    return render_template('results.html', results=results)


# For running locally without gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
