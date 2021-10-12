## Kmer Association Analysis

The goal of this particular module is to use algorithms to find which kmers are most associated with certain diseases.

This works in a series of 2 steps:

1. Calculating TF-IDF for all input csv files containing kmers & counts.
2. Using recursive feature elimination with a logistic regression model from scikit learn.
3. Lastly, a ranking for the selected features is added to a csv.

## Usage
* General Usage
```
python kmer_selector.py --config <Path to config> --output_prefix <output prefix name>
```
* Example Usage
```
python kmer_selector.py --config testing/config_test.config --output_prefix run_1
```