from sklearn.decomposition import TruncatedSVD
import numpy as np


class lsi():
    def __init__(self,t):

        svd = TruncatedSVD(n_components=100, random_state=42, algorithm='arpack')
        self.lsi = svd.fit_transform(t.w)

        self.members = t.db.get_all_names()

        mean_speeches = []
        for member in self.members:
            filters = {'member_name':member}
            ids = np.atleast_1d(t.db.get_ids_by_filters(filters)).astype(int)

            if len(ids) <= 5:
                mean = np.zeros(self.lsi.shape[1])
            else:
                mean = self.lsi[ids].mean(axis=0)

            mean_speeches.append(mean)

        mean_speeches = np.asarray(mean_speeches)

        # norms = np.linalg.norm(mean_speeches, axis=1, keepdims=True)
        # mean_speeches = mean_speeches / (norms + 1e-9)

        self.pairwise_similarity = mean_speeches @ mean_speeches.T
        np.fill_diagonal(self.pairwise_similarity, -1.0)

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