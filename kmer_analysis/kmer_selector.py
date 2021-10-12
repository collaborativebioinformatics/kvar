#!/usr/bin/env python3
"""
This file is the client for operating the TFIDF calculator,
saving the output, and using the TFIDF matrix.

Usage:
    python kmer_selector.py --config testing/config_test.config --output_prefix run_1
"""
import argparse
import AssociationFinder as AF
import pandas as pd 
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import numpy as np

def get_args():
    """
    This method parses the arguments for the kmer selector
    module.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        help="Path to config file for the kmer selection",
        required=True,
    )
    parser.add_argument(
        "--output_prefix",
        "-o",
        help="Prefix and path to the output files",
        required=True,
    )
    return parser.parse_args()

def get_kmer_scores(training_data, training_labels):
    """
    This method returns the scores for each feature in
    the training dataset.

    In particular, this utilizes recursive feature elimination
    using a logistic regression model from scikit learn. 
    """
    # start logistic regression model
    logreg_model = LogisticRegression()
    recFeatureElimination = RFE(logreg_model)
    recFeatureElimination = recFeatureElimination.fit(training_data, training_labels)

    # summarize the selection of the attributes
    return recFeatureElimination.ranking_

def main():
    args = get_args()
    print(args.config)

    # get TF-IDF for all input files.
    tfidf_obj: AF.AssociationFinder = AF.TFIDF_KvarFinder(args.config)
    training_x, training_y = tfidf_obj.obtain_tests_from_files()
    kmer2column = tfidf_obj.kmer2column

    # save numpy array to csv/
    pd.DataFrame(training_x, 
                 columns=kmer2column.keys(),
                 index=training_y).to_csv(args.output_prefix+"_TFIDF.csv", 
                                          header=True,
                                          index=True)

    # use logisitic regression for multivariate feature selection.
    kmer_ranking = get_kmer_scores(training_x, training_y)
    kmer_ranking_array = np.array([[list(kmer2column.keys())[i], kmer_ranking[i]] 
                                    for i in range(len(kmer_ranking))])
    pd.DataFrame(kmer_ranking_array,
                 columns=["kmer", "rank"]).to_csv(args.output_prefix+"_ranking.csv", header=True, index=False)

if __name__ == "__main__":
    main()