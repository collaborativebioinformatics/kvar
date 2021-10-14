#!/usr/bin/env python3
"""
Author: Dreycey Albin

This file is the client for operating the TFIDF calculator,
saving the output, and using the TFIDF matrix.

Usage:
    python3 kmer_selector.py --positive_file_path breast_cancer_testing/positive_dir \
                             --negative_file_path breast_cancer_testing/negative_dir \
                             --output BREAST_ANALYSIS \
                             --kmer_cutoff 1000 \
                             --fasta_out_path ./ranked_kmers.fa
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
        "--positive_file_path",
        "-pos",
        help="Path to postive directory",
        required=True,
    )
    parser.add_argument(
        "--negative_file_path",
        "-neg",
        help="Path to negative directory",
        required=True,
    )
    parser.add_argument(
        "--output_prefix",
        "-o",
        help="Prefix and path to the output files",
        required=True,
    )
    parser.add_argument(
    "--fasta_out_path",
    help="Output path for the fasta file.",
    required=True,
    )    
    parser.add_argument(
        "--kmer_cutoff",
        "-n",
        type=int,
        help="Number of kmers to evaluate in total [DEFAULT: 50,000]",
        required=False,
    )  
    parser.add_argument(
        "--add_tfidf_to_csv",
        help="Adds the TFIDF output to csv, aim for lower -n if using this!",
        required=False,
    )  
    parser.add_argument(
    "--read_kmers_backwards",
    help="Reads the tsv kmer file backwards (Avoid if possible!)",
    required=False,
    ) 
    return parser.parse_args()

def get_kmer_scores(training_data, training_labels):
    """
    This method returns the scores for each feature i
    the training dataset.

    In particular, this utilizes recursive feature elimination
    using a logistic regression model from scikit learn. 
    """
    # start logistic regression model
    logreg_model = LogisticRegression(penalty='l2') # using L2; ridge regression.
    step_size_for_rfe = int(len(training_data[0]) * 0.05)
    print("    Starting recursive feature selection..")
    recFeatureElimination = RFE(logreg_model, 
                                n_features_to_select=1,
                                step=step_size_for_rfe)
    recFeatureElimination = recFeatureElimination.fit(training_data, training_labels)
    print("         DONE.")

    return recFeatureElimination.ranking_

def ranksarray2fasta(ranking_array, fasta_path):
    """
    This method turns a ranked array into
    a fasta.
    """
    top_10_percent = int(len(ranking_array) * 0.10)
    with open(fasta_path, "w") as output_fasta:
        for count, row in enumerate(ranking_array):
            if count > top_10_percent:
                break
            kmer = row[0]
            ranking = row[1]
            output_fasta.write(f">{count}_{ranking} \n{kmer} \n")

def main():
    args = get_args()

    # get TF-IDF for all input files.
    if args.kmer_cutoff != None:
        tfidf_obj: AF.AssociationFinder = AF.TFIDF_KvarFinder(args.positive_file_path, 
                                                              args.negative_file_path,
                                                              args.kmer_cutoff)
    else: 
        tfidf_obj: AF.AssociationFinder = AF.TFIDF_KvarFinder(args.positive_file_path, 
                                                              args.negative_file_path)
    training_x, training_y = tfidf_obj.obtain_tests_from_files()
    kmer2column = tfidf_obj.kmer2column

    # save numpy array to csv/
    if (args.add_tfidf_to_csv):
        pd.DataFrame(training_x, 
                    columns=kmer2column.keys(),
                    index=training_y).to_csv(args.output_prefix+"_TFIDF.csv", 
                                            header=True,
                                            index=True)

    # use logisitic regression for multivariate feature selection.
    kmer_ranking = get_kmer_scores(training_x, training_y)
    kmer_ranking_array = [ [list(kmer2column.keys())[i], int(kmer_ranking[i])] 
                                     for i in range(len(kmer_ranking))
                                  ]

    print("    Reading file, saving kmers..")
    kmer_ranking_df = pd.DataFrame(kmer_ranking_array, columns=["kmer", "rank"])
    sorted_df = kmer_ranking_df.sort_values(by="rank", ascending=True)
    sorted_df.to_csv(args.output_prefix+"_ranking.csv", header=True, index=False)
    print("         DONE.")

    print("    Reading file, saving kmers..")
    ranksarray2fasta(np.array(sorted_df), args.fasta_out_path)
    print("         DONE.")

if __name__ == "__main__":
    main()