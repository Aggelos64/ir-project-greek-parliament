from flask import g,Flask, render_template, request, redirect
import webbrowser
import tfidf
import quarry_database as qd
import create_database
import generate_subset
from keywords import top_words
import lsi
import pickle

db_name = 'set.db'
csv_name= 'Greek_Parliament_Proceedings_1989_2020.csv'

create_database.createdb(csv_name, db_name)

# load tfidf module and cache it
try:
    with open("cached_tfidf", "rb") as f:
        tfidf_module = pickle.load(f)
except FileNotFoundError:
    tfidf_module = tfidf.tfidf(db_name)

    with open("cached_tfidf", "wb") as f:
        pickle.dump(tfidf_module, f)

# load lsi module and cache it
try:
    with open("cached_lsi", "rb") as f:
        lsi_module = pickle.load(f)
except FileNotFoundError:
    lsi_module = lsi.lsi(tfidf_module)

    with open("cached_lsi", "wb") as f:
        pickle.dump(lsi_module, f)


def get_db():
    if "db" not in g:
        g.db = qd.quarry_db(db_name)
    return g.db

app = Flask(__name__)

webbrowser.open("http://localhost:5000/")


@app.route('/')
def index():
    query = request.args.get('q', '')
    date_from = request.args.get('from', '')
    date_to = request.args.get('to', '')

    filters = {}

    if date_from != '':
        filters['date_from'] = date_from
    
    if date_to != '':
        filters['date_to'] = date_to

    results = None
    db = get_db()

    if query != '':
        results = db.get_by_idarray(tfidf_module.search(query,filters=filters))
    
    names = db.get_all_names()
    partys = db.get_all_partys()
    return render_template('index.html', results=results,names=names,partys=partys)


@app.route('/keywords')
def keywords():
    member = request.args.get('member', '')
    party = request.args.get('party', '')    
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * 10

    filters = None
    if member != '':
        filters = {'member_name':member}
        query = {'member':member}
    if party != '':
        filters = {'political_party':party}
        query = {'party':party}
    if not filters:
        return redirect('/')
    
    db = get_db()
    results,total_pages = db.get_speeches_by_filters(filters=filters, offset=offset)
    keywords = top_words(tfidf_module,filters)
    return render_template('keywords.html', results=results, keywords=keywords, page=page, total_pages=total_pages, filters=query)


@app.route('/pairs')
def pairs():
    k = request.args.get('pairs_k', 10, type=int)

    results = lsi_module.topk_pairs(k)
    return render_template('pairs.html', results=results)

if __name__ == '__main__':
    app.run(debug=False)
