This directory contains 5 python files with the following functions:

- sentiment-cardiffnlp.py : This file contains the code to run the sentiment analysis using the cardiffnlp model. 

- sentiment-finiteautomata.py : This file contains the code to run the sentiment analysis using the finiteautomata model.

- sentiment-seethal.py : This file contains the code to run the sentiment analysis using the seethal model.

- combine_results.py: This function takes post_id as input and reads the corresponding comments file and combines the results of the three models and writes the output to a single file  

- annotate_sampler.py: Takes the cmbined dataset as the input. It contains all the comments from the 100 posts (5.7k) and samples 100 comments (34 positive, 33 negative, 33 neutral) and writes the output to a single file  