#!/usr/bin/env python3
"""
Author: Dreycey Albin

The purpose of this module is to create a strategy/template pattern that
uses an algorithm for finding kmers highly associated with certain phenotypes. 
In particular, the kmers output from previous modules are imported using a CSV,
and those kmer frequencies per file are transformed using an in-house TF-IDF.


Software Design Patterns used: 
    1. template pattern
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Set, Tuple
from pathlib import Path
import configparser
from os import listdir
from os.path import isfile, join
import numpy as np
from tqdm import tqdm




class AssociationFinder(ABC):
    """ 
    This abstract class outline the template 
    for the association finding algorithm. 
    """

    @property
    @abstractmethod
    def samples_to_review(self):# -> List[Path]:
        """ This is the algorithm used """
        pass

    @abstractmethod
    def obtain_tests_from_files(self, x_vector):# -> Tuple(List[List[int]], List[str]):
        """
        This abstract method works to find kmers that 
        are associated with specific disease states
        and returns a dictionary of kmers and their algorithm
        associated values.

        Args:
            param1 (int): The first parameter.

        Returns:
            1. a Matrix of the vectors for training.
            2. a list of binary labels.
        """
        pass

class TFIDF_KvarFinder(AssociationFinder):
    """ 
    TFIDF is used here to find kmers associated with 
    specific fastq files.
    This takes in normalized counts and performs TF-IDF.
    """

    def __init__(self, pos_dir, neg_dir, kmer_cutoff=50000, readbackwards=False):
        # finished
        self.pos_dir = pos_dir
        self.neg_dir = neg_dir
        self.kmer_cutoff = kmer_cutoff
        self.readbackwards = readbackwards
        self.doc2kmerfreqs: Dict[str, Dict[str, float]] = {}
        self.unique_kmers: Set = set()
        self._samples_to_review: List[Path] = [] # DONE
        self.training_tfidf = np.array([]) 
        self.training_labels = np.array([]) # Done
        # inefficient (memory) mapping dictionaries.
        self.sample2row = {}
        self.row2sample = {}
        self.kmer2column = {} 
        self.column2kmer = {} 

        # initialize 
        self.initializer()

    @property
    def samples_to_review(self) -> List[Path]:
        """ This is the algorithm used """
        return self._samples_to_review

    @samples_to_review.setter
    def samples_to_review(self, samples: List[Path]) -> None:
        self._samples_to_review = samples

    def initializer(self) -> None:
        """
        This method initilizes the TFIDF datastructure/object
        """
        print("Starting a new TFIDF Analysis..")
        pos_dir = self.pos_dir
        neg_dir = self.neg_dir
        pos_files = [join(pos_dir, f) for f in listdir(pos_dir) if isfile(join(pos_dir, f))]
        neg_files = [join(neg_dir, f) for f in listdir(neg_dir) if isfile(join(neg_dir, f))]

        # Create label vector
        self.training_labels = np.zeros((len(pos_files)+len(neg_files)))
        for ind in range(len(pos_files)):
            self.training_labels[ind] = 1

        # Create Sample2row map
        self.sample2row = {file_path : row_n for row_n, file_path in 
                                                enumerate(list(pos_files+neg_files))}
        self.row2sample = {row_n : file_path for row_n, file_path in 
                                                enumerate(list(pos_files+neg_files))}
        # Set samples to review
        self.samples_to_review = [Path(sample_file) for sample_file in self.sample2row.keys()]
        
        # make data sets
        print("    Reading file, saving kmers..")
        self.doc2info()
        print("         DONE!")
        print("    Obtaining mapping for unique kmers..")
        self.get_kmer2column()
        print("         DONE!")

    def doc2info(self, delimiter="\t") -> None:
        """
        This method takes in a CSV with kmers.

        Args:
            param1 (int): CSV with filtered kmers and frequencies
            Example:
                    ATGCTAGACTG, 0.3
                    ...
                    ATGCTAAACTG, 0.5
        Returns:
            None - updates class attributes
        TODO:
            1. This will be very slow, could be parallelized per file.
        """
        kmers_per_sample = int(self.kmer_cutoff / len(self.samples_to_review))
        print(f"        Kmers being used per sample: {kmers_per_sample}")
        for file_path in tqdm(self.samples_to_review):
            self.doc2kmerfreqs[str(file_path)] = {}
            with open(file_path) as csv_file:
                if self.readbackwards:
                    csv_lines = [x for x in csv_file.readlines()[::-1][:kmers_per_sample]]
                else:
                    try:
                        csv_lines = [next(csv_file) for x in range(kmers_per_sample)]
                    except StopIteration:
                        with open(file_path) as csv_file:
                            csv_lines = csv_file.readlines()
                        print(f"Kvar WARNING: only obtaining {len(csv_lines)}")
                for kmer_count, csv_row in enumerate(csv_lines):
                    kmer, freq = csv_row.strip("\n").split(delimiter)
                    print(kmer, freq)
                    if float(freq) > 0:
                        self.doc2kmerfreqs[str(file_path)][kmer] = float(freq) # assumes unique kmers
                        self.unique_kmers.add(kmer)

    def get_kmer2column(self):
        """
        This method creates a mapping from kmers to specific columns/rows.
        """
        for col_index, kmer in enumerate(self.unique_kmers):
            self.kmer2column[kmer] = col_index
            self.column2kmer[col_index] = kmer

    def obtain_tests_from_files(self) -> List[List[int]]:
        """
        This abstract method works to find kmers that 
        are associated with specific disease states
        and returns a dictionary of kmers and their algorithm
        associated values.

        Args:
            param1 (int): The first parameter.

        Returns:
            1. a Matrix of the vectors for training.
            2. a list of binary labels.
        """
        tfidf_matrix = np.zeros((len(self.training_labels), len(self.unique_kmers)))
        print("    Calculating TFIDF..")
        for row in tqdm(range(len(self.training_labels))):
            for column in range(len(self.unique_kmers)):
                tfidf_matrix[row, column] = self.calculate_tfidf(row, column)
        print("         DONE!")
        return tfidf_matrix, self.training_labels

    def calculate_tfidf(self, row, column):
        """
        This method calculates a the tf-idf for a particular 
        element in the TFIDF matrix. 
        """
        sample = self.row2sample[row]
        kmer = self.column2kmer[column]
        raw_count = self.doc2kmerfreqs[sample][kmer] if kmer in self.doc2kmerfreqs[sample] else 0
        term_frequency = raw_count / sum(self.doc2kmerfreqs[sample].values())
        doc_frequency = self.count_samples_with_kmer(kmer) / len(self.training_labels)
        tf_idf =  term_frequency * np.log(1 / doc_frequency)
        return tf_idf

    def count_samples_with_kmer(self, kmer):
        """
        counts number of samples with a particular kmer.
        """
        return sum([1 for sample in self.doc2kmerfreqs.values() if kmer in sample.keys()])