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
IN_DIR = "out/combined"
LABELS = ['negative', 'neutral', 'positive']
COLUMNS_TO_DROP = ['MODEL_LABEL_CARDIFFNLP', 'MODEL_LABEL_FINITEAUTOMATA', 'MODEL_LABEL_SEETHAL', 'MODEL_MAJORITY']
OUT_DIR = "out"
n_pos = 34
n_neg = 33
n_neu = 33
RANDOM_STATE = 42
#################################################

assert n_pos + n_neg + n_neu == 100

def sample(df):
    """
       Takes the cmbined dataset as the input. It contains all the comments from the 100 posts (5.7k)
         and samples 100 comments (34 positive, 33 negative, 33 neutral) and writes the output to a single file  
    """
    df_pos = df[df['MODEL_MAJORITY'] == 'positive'].sample(n=n_pos)
    df_neg = df[df['MODEL_MAJORITY'] == 'negative'].sample(n=n_neg)
    df_neu = df[df['MODEL_MAJORITY'] == 'neutral'].sample(n=n_neu)
    print("Number of positive comments: ", len(df_pos))
    print("Number of negative comments: ", len(df_neg))
    print("Number of neutral comments: ", len(df_neu))
    df = pd.concat([df_pos, df_neg, df_neu], axis=0)
    df = df.loc[:,~df.columns.duplicated()]
    df.to_csv(f'{OUT_DIR}/annotate_with_model_label.csv', index=False)
    print("annotate_with_model_label.csv columns", df.columns)
    df = df.drop(columns=COLUMNS_TO_DROP)
    df.to_csv(f'{OUT_DIR}/annotate.csv', index=False)
    print("annotate.csv columns", df.columns)
    

if __name__ == "__main__":
    posts_df = pd.read_csv(f'{BASE_DIR}/posts.csv') # Reads the post ids in the dataset
    print("Number of posts in the dataset: ", len(posts_df))

    combined_df = pd.DataFrame(columns=['COMMENT_ID', 'COMMENT_PARENT_ID', 'COMMENT_SCORE', 'COMMENT_DEPTH',
       'COMMENT_CREATED_TIMESTAMP', 'AUTHOR_USERNAME', 'COMMENT_TEXT_CONTENT',
       'MODEL_LABEL_CARDIFFNLP', 'MODEL_LABEL_FINITEAUTOMATA',
       'MODEL_LABEL_SEETHAL', 'MODEL_MAJORITY']) # Setting up the combined dataset

    # Combines the 100 post files into a single dataframe
    for i in range(0, len(posts_df)):
        post_id = posts_df.iloc[i]['POST_ID']
        print(f"{i+1}. Processing post: {post_id}")
        df = pd.read_csv(f'{IN_DIR}/{post_id}.csv')
        combined_df = pd.concat([combined_df, df], axis=0)

    print("Total number of comments: ", len(combined_df))
    # Randomize the order of the comments with some random state
    combined_df = combined_df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    # Function call to sample the comments and write the output to a single file
    sample(combined_df)
