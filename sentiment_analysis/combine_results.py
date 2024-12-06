# Code: Combine the results
# Label: Labels: 0 -> Negative; 1 -> Neutral; 2 -> Positive
# Author: Kowsik Nandagopan D
# Date: 22-08-2023

import pandas as pd
import numpy as np
import os
from collections import Counter

#################################################
BASE_DIR = "../"
IN_DIRS = [
    "out/cardiffnlp",
    "out/finiteautomata",
    "out/seethal",
]
MODEL_NAMES = ["CARDIFFNLP", "FINITEAUTOMATA", "SEETHAL"]
LABELS = ['negative', 'neutral', 'positive']
OUT_DIR = "out/combined"
#################################################

def voter(x):
    """
    x is the row of the dataframe
    output of this function is the majority label of the three models     
    """
    labels = x[[f"MODEL_LABEL_{model}" for model in MODEL_NAMES]].tolist()
    return Counter(labels).most_common(1)[0][0]

def combine_results(post_id):
    """
       This function takes post_id as input and reads the corresponding comments file 
       and combines the results of the three models and writes the output to a single file  
    """
    dfs = []
    for IN_DIR in IN_DIRS:
        dfs.append(pd.read_csv(f'{IN_DIR}/{post_id}.csv'))
    df = pd.concat(dfs, axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    df["MODEL_MAJORITY"] = df.apply(voter, axis=1)
    df.to_csv(f'{OUT_DIR}/{post_id}.csv', index=False)

if __name__ == "__main__":
    posts_df = pd.read_csv(f'{BASE_DIR}/posts.csv') # Reads the post ids in the dataset
    print("Number of posts in the dataset: ", len(posts_df))

    for i in range(0, len(posts_df)):  # Reads each file in the post_id comment and combines the results
        post_id = posts_df.iloc[i]['POST_ID']
        print(f"{i+1}. Processing post: {post_id}")
        combine_results(post_id)

