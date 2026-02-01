import quarry_database as qd
import numpy as np
from text_processor import text_process,map_stems
from multiprocessing import Pool
from inverse_cat import inverse
from scipy.sparse import lil_matrix
import math


# tfidf class calculates the wights in the dataset
# self.w contains the weights
# self.db has an instance of the database
# self.stem_map has a map of stems to first original word
# self.terms has a list of all tokens
# self.idf has all the document frequencies
class tfidf():
    
    def __init__(self,db='set.db'):
        self.db_name = db
        self.db = qd.quarry_db(db)
        df = self.db.get_all_speachees()

        self.stem_map = map_stems(df)

        with Pool() as pool:
            df = np.array(pool.map(text_process, df), dtype=object)

        cat = inverse(df)

        self.terms = list(cat.keys())

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
    def search(self,quary,k=20,filters=None):

        qw = self.process_quary(quary)

        if not filters:
            scores = self.w.dot(qw.T).toarray().ravel()
            top_docs = scores.argsort()[::-1][:k]
        else:
            rows = self.db.get_ids_by_filters(filters)
            scores = self.w[rows, :].dot(qw.T).toarray().ravel()
            top_docs = scores.argsort()[::-1][:k]
            top_docs = rows[top_docs]


        return (top_docs).tolist()
    
    # returns the weight matrix of speeches with some filters or by ids
    # filters : Dictionary containing filter criteria. Can include:
    #    member_name : Filter by speaker name
    #    date_from : Start date (YYYY-MM-DD)
    #    date_to : End date (YYYY-MM-DD)
    #    political_party : Filter by political party
    def getw_by_filters(self,filters=None,ids=None):
        if not ids:
            rows = self.db.get_ids_by_filters(filters)
        else:
            rows = ids
        return self.w[rows, :]
    
    # turns the quarry to weight vector
    def process_quary(self,quary):
        quary = text_process(quary)

        q_inv = inverse([quary])

        qtf = lil_matrix((1, len(self.terms)), dtype=np.float32)

        for i, term in enumerate(self.terms):
            if term in q_inv:
                qtf[0,i] = 1+ math.log(q_inv[term][0])

        qw = qtf.multiply(self.idf)
        return qw
    
    # getstate for caching
    def __getstate__(self):
        state = self.__dict__.copy()
        state["db"] = None
        return state
    
    # setstate for caching
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.db = qd.quarry_db(self.db_name)
