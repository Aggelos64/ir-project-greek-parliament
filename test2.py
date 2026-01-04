import tfidf
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity


s = tfidf.tfidf('subset2000.db')

w = s.getw()

svd = TruncatedSVD(n_components=100, random_state=42, algorithm='arpack')
X_lsi = svd.fit_transform(w)

qw = s.process_quary("οικονομικο σκανδαλο")
q_lsi = svd.transform(qw)

similarities = cosine_similarity(q_lsi, X_lsi).flatten()
top_indices = similarities.argsort()[::-1][:5]
results = s.db.get_by_idarray(top_indices)

print(results)

