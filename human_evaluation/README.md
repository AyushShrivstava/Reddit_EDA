## HUMAN EVALUATION

This directory contains following files and directories.

### *.csv:
Each .csv in this directory has few common fields and are as follows:
   * COMMENT_ID: Comment ID of the comment
   * COMMENT_PARENT_ID: Parent ID of the comment annotated.
   * COMMENT_SCORE: It represents the comment score of the comment.
   * COMMENT_DEPTH: The depth of the comments
   * COMMENT_CREATED_TIMESTAMP: The time at which the comments are created
   * AUTHOR_USERNAME: It represents username of the author.
   * COMMENT_TEXT_CONTENT: It contains the comment data.
   * 22210036: Roll No. of Annotator 1, who annotated the 100 samples.

1. `human_eval.csv`: csv file for annotators to lables 100 random sample from comment corpus. The additional fields are as follows:
   
   * 22210036: Roll No. of Annotator 1, who annotated the 100 samples.
   * 22210034:  Roll No. of Annotator 2, who annotated the 100 samples.
   * 22210019:  Roll No. of Annotator 3, who annotated the 100 samples.
   * ANNOTATORS_MAJORITY: It represents the majority vote of all the annotators.

2. `model_labels.csv`: csv file contains the labels predicted by all the models. The additional fields of the csv are as follows:
   
   * MODEL_LABEL_CARDIFFNLP: Model Predictions made by model named as ```CARDIFFNLP```
   * MODEL_LABEL_FINITEAUTOMATA: Model Predictions made by model named as ```FINITEAUTOMATA```
   * MODEL_LABEL_SEETHAL: Model Predictions made by model named as ```SEETHAL```
   * MODEL_MAJORITY: It represents the majority vote of all the models.

3. `model_vs_ann.csv`: The additional fields in this csv are as follows:
   
   * MODEL_LABEL_CARDIFFNLP: Model Predictions made by model named as ```CARDIFFNLP```
   * MODEL_LABEL_FINITEAUTOMATA: Model Predictions made by model named as ```FINITEAUTOMATA```
   * MODEL_LABEL_SEETHAL: Model Predictions made by model named as ```SEETHAL```
   * MODEL_MAJORITY: It represents the majority vote of all the models.
   * ANNOTATORS_MAJORITY: It represents the majority vote of all the annotators.

4. `model_annotate_mismatch.ipynb`: This notebook contains the comparision of model and annotators majority labels.
   * the comparision consists of `42` mismatched sample and `58` matched samples.
   * pie-charts are created to display the distribution of labels in models and annotators annotations.
  