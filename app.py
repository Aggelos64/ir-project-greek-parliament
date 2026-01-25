from flask import g,Flask, render_template, request, redirect
import webbrowser
import tfidf
import quarry_database as qd
import create_database
import generate_subset
from keywords import top_words
import lsi

db_name = 'subset2000.db'
csv_name= 'subset2000.csv'

generate_subset.make_csv('Greek_Parliament_Proceedings_1989_2020.csv',csv_name,n=2000)

create_database.createdb(csv_name, db_name)
s = tfidf.tfidf(db_name)
lsi_module = lsi.lsi(s)

def get_db():
    if "db" not in g:
        g.db = qd.quarry_db(db_name)
    return g.db

app = Flask(__name__)

# webbrowser.open("http://localhost:5000/")


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
        results = db.get_by_idarray(s.search(query,filters=filters))
    
    names = db.get_all_names()
    partys = db.get_all_partys()
    return render_template('index.html', results=results,names=names,partys=partys)


@app.route('/keywords')
def keywords():
    member = request.args.get('member', '')
    party = request.args.get('party', '')

    filters = None
    if member != '':
        filters = {'member_name':member}
    if party != '':
        filters = {'political_party':party}
    if not filters:
        return redirect('/')
    
    db = get_db()
    results = db.get_by_idarray(db.get_ids_by_filters(filters=filters))
    keywords = top_words(s,filters)
    return render_template('keywords.html', results=results, keywords=keywords)


@app.route('/pairs')
def pairs():
    k = int(request.args.get('pairs_k', ''))

    results = lsi_module.topk_pairs(k)
    return render_template('pairs.html', results=results)

if __name__ == '__main__':
    app.run(debug=False)
