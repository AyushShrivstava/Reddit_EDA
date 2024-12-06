# Library imports
import numpy as np
import pandas as pd

def calc_disagreements(bin_count):
    # Calculate the number of disagreements for a given bin count
    XXt = np.outer(bin_count, bin_count)
    XXt -= np.diag(np.diag(XXt))
    n_disagreements = np.sum(XXt)/2
    return n_disagreements

def krippendorff_alpha_nominal(response_matrix):
    # Calculate Krippendorff's alpha for nominal values, with 0 indicating non-response
    
    n_items, n_annotators = np.shape(response_matrix)
    n = n_items * n_annotators

    item_disagreements = np.array([calc_disagreements(np.bincount(response_matrix[i, :],minlength=4)[1:]) for i in range(n_items)])

    D_o = np.sum(item_disagreements / (n_annotators-1)) / float(n)

    counts = np.bincount(response_matrix.reshape(n_items * n_annotators))
    D_e = calc_disagreements(counts) / (n*(n-1))

    alpha = 1 - D_o / D_e
    return alpha

# Reading Data from Human evaluation file
data = pd.read_csv('human_evaluation/human_eval.csv', usecols=['22210019', '22210034','22210036'])

# Assigning 3 - Positive , 2 - Neutral, 1 - Negative
def convert_to_response(rating):
    if rating == 'Positive':
        return 3
    elif rating == 'Neutral':
        return 2
    elif rating == 'Negative':
        return 1
    else:
        return None  # Handle any other cases here

# Converting the data to response matrix
data = data.applymap(convert_to_response)

# Calculating Krippendorff's alpha
alpha = krippendorff_alpha_nominal(data.values)

# Printing the value of alpha
print(alpha)