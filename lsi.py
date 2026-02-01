from sklearn.decomposition import TruncatedSVD
import numpy as np

# the lsi class performs svd in the tfidf weights, calculates a mean speech for each party member and a pairwise similarity between the mean speeches
class lsi():
    def __init__(self,tfidf):
        # SVD
        svd = TruncatedSVD(n_components=100, random_state=42, algorithm='arpack')
        lsi = svd.fit_transform(tfidf.w)

        self.members = tfidf.db.get_all_names()

        # calculate mean speech for each member
        mean_speeches = []
        for member in self.members:
            filters = {'member_name':member}
            ids = np.atleast_1d(tfidf.db.get_ids_by_filters(filters)).astype(int)

            if len(ids) <= 5:
                mean = np.zeros(lsi.shape[1])
            else:
                mean = lsi[ids].mean(axis=0)

            mean_speeches.append(mean)

        mean_speeches = np.asarray(mean_speeches)

        #calculate pairwise similarity
        self.pairwise_similarity = mean_speeches @ mean_speeches.T
        np.fill_diagonal(self.pairwise_similarity, -1.0)

    # returns top k most simmular pairs of parliment members
    def topk_pairs(self, k=10):
        n = self.pairwise_similarity.shape[0]
        
        # upper triangle to avoid duplicates
        triu_i, triu_j = np.triu_indices(n, k=1)
        scores = self.pairwise_similarity[triu_i, triu_j]

        idx = np.argpartition(scores, -k)[-k:]

        pairs = [
            (self.members[triu_i[i]], self.members[triu_j[i]], scores[i])
            for i in idx
        ]

        # sort final k
        pairs.sort(key=lambda x: x[2], reverse=True)
        return pairs