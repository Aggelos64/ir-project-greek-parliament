# generate_subset.py generates a subset of the Greek_Parliament_Proceedings_1989_2020.csv file
# use load_set to get the subset
# use make_csv to save the subset as a csv file

import pandas as pd

# load_set generates a subset and returns it
# file = csv file with data
# n = amount of samples. n=0 for all
# split = sampling method. 'nth' for every nth element 'rand' for random
def load_set(file,n=0,split='rand'):
    df = pd.read_csv(file)
    if(n == 0):
        return df
    if(split == 'nth'):
        k = round(df.shape[0]/n)
        return df.iloc[::k]
    return df.sample(n=n)

# make_csv generates a subset and saves it as a csv file
# name = name of the csv file ('example.csv')
# n = amount of samples. n=0 for all
# split = sampling method. 'nth' for every nth element 'rand' for random
def make_csv(name,n=0,split='rand'):
    subset = load_set(n=0,split='rand')
    subset.to_csv(name, index=False)