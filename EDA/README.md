# Exploratory Data Analysis of r/srilanka


This directory aims to explore the trends in the data collected from the subreddit r/srilanka.Exploration of the data is done at two levels. First the EDA was done at post level. Second the EDA was done to identify the trends in the comments. This directory contains following files and directories:

* **`Combine_Comments_CSV.ipynb`** : This notebook reads all the comment files from  `../comments` directory and  combines all the csv files into one csv file. The combined csv file is stored in the directory `Corpus`. 
* **`Corpus`** : This directory contains the combined Comment's text corpus and Post's text Corpus.
    * `Comments_Corpus.csv` : This csv file contains the combined Comment's text corpus.
    * `Posts_Corpus.csv` : This csv file contains the combined Post's text corpus.
* **`EDA_Comments.ipynb`** : This notebook analyses the entire Comment's text corpus and displays the trends in the comments.
* **`EDA_Posts.ipynb`** : This notebook analyses the entire Post's text corpus and displays the trends in the posts.
* **`Convert_to_HTML.ipynb`** : This notebook converts the `EDA_Comments.ipynb` and `EDA_Posts.ipynb` files to HTML files.
* **`EDA_Comments.html`** : This is the HTML version of the `EDA_Comments.ipynb` file.
* **`EDA_Posts.html`** : This is the HTML version of the `EDA_Posts.ipynb` file.