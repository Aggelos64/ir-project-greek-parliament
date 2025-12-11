import quarry_database as qd
import numpy as np
from text_processor import text_process
from multiprocessing import Pool
from inverse_cat import inverse
from scipy.sparse import lil_matrix
import math



class tfidf():
    
    def __init__(self,db='set.db'):
        self.db = qd.quarry_db(db)
        df = self.db.get_all_speachees()

        with Pool() as pool:
            df = np.array(pool.map(text_process, df), dtype=object)

        cat = inverse(df)

        self.terms = cat.keys()
        
        # calculate all (N+1)/dft
        self.idf = np.log((df.shape[0] + 1) / np.array([len(cat[t]) for t in cat]))

        tfs = lil_matrix((df.shape[0], len(cat.keys())), dtype=np.float32)

        for i, term in enumerate(cat.keys()):
            for doc ,ft in cat[term].items():
                tfs[doc,i] = 1 + math.log(ft)

        # make weight matrix
        tfs = tfs.tocsr()
        self.w = tfs.multiply(self.idf)
        self.w = self.w.tocsr()

    
    # filters : Dictionary containing filter criteria. Can include:
    #    member_name : Filter by speaker name
    #    date_from : Start date (YYYY-MM-DD)
    #    date_to : End date (YYYY-MM-DD)
    #    political_party : Filter by political party
    def search(self,quarry,k=20,filters=None):
        quarry = text_process(quarry)

        q_inv = inverse([quarry])

        qtf = lil_matrix((1, len(self.terms)), dtype=np.float32)

        for i, term in enumerate(self.terms):
            if term in q_inv:
                qtf[0,i] = 1+ math.log(q_inv[term][0])

        qw = qtf.multiply(self.idf)

        if not filters:
            scores = self.w.dot(qw.T).toarray().ravel()
            top_docs = scores.argsort()[::-1][:k]
        else:
            rows = self.db.get_ids_by_filters(filters)
            scores = self.w[rows, :].dot(qw.T).toarray().ravel()
            top_docs = scores.argsort()[::-1][:k]
            top_docs = rows[top_docs]


        return (top_docs+1).tolist()
