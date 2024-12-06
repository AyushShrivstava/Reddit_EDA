# Code: Sentiment analysis using cardiffnlp/twitter-roberta-base-sentiment-latest model
# Label: Labels: 0 -> Negative; 1 -> Neutral; 2 -> Positive
# Author: Kowsik Nandagopan D
# Date: 22-08-2023
# Reference: 

import pandas as pd
import numpy as np
import os
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from rich.pretty import pprint

#################################################
MODEL_PATH = "cardiffnlp/twitter-roberta-base-sentiment-latest" # Loading the required model
BASE_DIR = "../"
OUT_DIR = "out/cardiffnlp"
CUDA = "0"
BATCH_SIZE = 32
MAX_TOKENS = 512
LABELS = ['negative', 'neutral', 'positive']
MODEL_NAME = MODEL_PATH.split('/')[0].upper()
#################################################
os.environ["CUDA_VISIBLE_DEVICES"] = CUDA

device = f"cuda:{CUDA}" if torch.cuda.is_available() else "cpu"

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH).to(device)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model.eval()

# print(model)
# print(tokenizer)
# exit()

class CommentsData(Dataset):
    """
       Dataset class for the comments  
    """
    def __init__(self, csv_file):
        """
        Takes the path to the csv_file(str) and stores in the data attribute of this class
        the data attribute is a list of dictionaries. Each dictionary contains the comment (tokenised) and the comment_id 
        """
        self.comments_df = pd.read_csv(csv_file)
        print("Number of comments in the dataset: ", len(self.comments_df))
        self.data = []
        for i in range(0, len(self.comments_df)):
            comment = self.comments_df.iloc[i]
            # print(comment['COMMENT_TEXT_CONTENT'])
            self.data.append({
                'comment': tokenizer.encode(comment['COMMENT_TEXT_CONTENT'], add_special_tokens=True, max_length=MAX_TOKENS, truncation=True, padding='max_length', return_tensors='pt'),
                'id': comment['COMMENT_ID'],
            })

    def write_predictions(self, labels):
        """
        Given the predictions(labels) for the comments, this function writes the predictions to a csv file 
        """
        label = pd.Series(labels)
        self.comments_df[f'MODEL_LABEL_{MODEL_NAME}'] = label
        self.comments_df.to_csv(f'{OUT_DIR}/{post_id}.csv', index=False)

    def __len__(self):
        """
        Sends the length of the comments dataframe 
        """
        return len(self.comments_df)

    def __getitem__(self, idx):
        """
        Sends the comment for the given index 
        """
        return self.data[idx]['comment']


if __name__ == "__main__":

    posts_df = pd.read_csv(f'{BASE_DIR}/posts.csv') # Reads the post ids in the dataset
    print("Number of posts in the dataset: ", len(posts_df))

    for i in range(0, len(posts_df)): # Reads each file in the post_id comment and predicts the sentiment
        post_id = posts_df.iloc[i]['POST_ID']
        # Check file exists
        print (f"{i+1}. Processing comments for the post: ", post_id) 
        comments_path = f'{BASE_DIR}/comments/{post_id}.csv'
        if not os.path.isfile(comments_path):
            print("Comments file not found for the post: ", post_id)
            continue
        # Load comments
        data = CommentsData(comments_path)
        # Data loader for the comments
        data_loader = DataLoader(data, batch_size=BATCH_SIZE, shuffle=False)

        # Predict
        predictions = []
        for batch in data_loader:
            batch = batch.reshape(-1, MAX_TOKENS)
            batch = batch.to(device)
            with torch.no_grad():
                outputs = model(batch)
            predictions.extend(outputs.logits.argmax(dim=-1).cpu().numpy().tolist())

        print("Number of predictions: ", len(predictions))
        # Assigns the labels corresponding to the predictions
        labels = [LABELS[prediction] for prediction in predictions]
        # Write predictions to file
        print("Writing predictions to file")
        data.write_predictions(labels)


