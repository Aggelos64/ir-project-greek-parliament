import numpy as np

# function that returns for each speech the k most important words by finding the biggest tfidf values
# tfidf: instance of tfidf
# returns the weight matrix of speeches with some filters or by ids
# filters : Dictionary containing filter criteria. Can include:
#    member_name : Filter by speaker name
#    date_from : Start date (YYYY-MM-DD)
#    date_to : End date (YYYY-MM-DD)
#    political_party : Filter by political party
def top_words(tfidf,filters, k=10):
    results = []
    # get the weights
    X = tfidf.getw_by_filters(filters)

    for i in range(X.shape[0]):
        # find indexes in sparse matrix
        start = X.indptr[i]
        end = X.indptr[i + 1]

        # if empty
        if start == end:
            results.append([])
            continue

        data = X.data[start:end]
        indices = X.indices[start:end]

        # get top k 
        if len(data) <= k:
            top = list(zip(indices, data))
        else:
            idx = np.argpartition(data, -k)[-k:]
            top = list(zip(indices[idx], data[idx]))

        # sort and add to results
        top.sort(key=lambda x: x[1], reverse=True)
        results.append([(tfidf.stem_map.get(tfidf.terms[i]), w) for i, w in top])

    return results