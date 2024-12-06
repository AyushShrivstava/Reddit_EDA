from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

# Set up stopwords and mask
stopwords = set(STOPWORDS)
mask = np.array(Image.open('imagemask.jpg'))

# Define the folder path
folder_path = '../comments'

# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Concatenate content from all CSV files
combined_content = ''
for csv_file in csv_files:
    data_file = pd.read_csv(os.path.join(folder_path, csv_file))
    combined_content += ' '.join(data_file['COMMENT_TEXT_CONTENT']) + ' '

# Generate the word cloud
wordcloud = WordCloud(
    stopwords=stopwords,
    min_word_length=3,  # Minimum word length set to 3
    width=1600,
    height=800,
    mask=mask,
    background_color="white",
    colormap="Set2"
).generate(combined_content)

# Create a plot for the word cloud
plt.figure(figsize=(20, 10), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)

# Show the plot
wordcloud.to_file ('word_cloud.pdf')
plt.show()
