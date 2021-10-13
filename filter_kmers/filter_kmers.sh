#!/usr/bin/bash

set -e

minkmercov=$1
input=$2
output=$3

if [ "$#" -ne 3 ]; then
  echo "  Usage: bash filter_kmers.sh min_kmer_cov input output " >&2 ;
  echo "Exiting now!!!"
  exit 1 ;
fi

echo "  Removing likely erroneous k-mers "
awk -F "\t" -v var=$minkmercov '{if($2>var){print}}' $input > $output
