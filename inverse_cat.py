
# creates an inverse document index as a dictionary with tokens as keys and
# as value a dictionary of docs and amount of apperances on each doc
def inverse(docs):
    apperances = {}

    # genereate a simple dict with the apperances of each term
    for docnum, doc in enumerate(docs):
        tokens = doc.split()

        for token in tokens:
            if token not in apperances:
                apperances[token] = []
            if token in apperances:
                apperances[token].append(docnum)
    
    # combine each apperances of the same doc
    for key in apperances:
        dic = {}
        for item in apperances[key]:
            if item not in dic:
                dic[item] = 0
            if item in dic:
                dic[item] = dic[item]+1
        apperances[key] = dic

    return apperances
