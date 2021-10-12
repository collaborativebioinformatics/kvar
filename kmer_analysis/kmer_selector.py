#!/usr/bin/env python3
"""
This file is the client for operating the TFIDF calculator,
saving the output, and using the TFIDF matrix.

Usage:
    python kmer_selector.py --config testing/config_test.config 
"""
import argparse
import AssociationFinder as AF
import pandas as pd 



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

def main():
    args = get_args()
    print(args.config)

    # get TF-IDF for all input files.
    tfidf_obj: AF.AssociationFinder = AF.TFIDF_KvarFinder(args.config)
    training_x, training_y = tfidf_obj.obtain_tests_from_files()
    kmer2column = tfidf_obj.kmer2column

    # save numpy array to csv
    pd.DataFrame(training_x, 
                 columns=kmer2column.keys(),
                 index=training_y).to_csv(args.output_prefix+".csv", 
                                          header=True,
                                          index=True)

if __name__ == "__main__":
    main()