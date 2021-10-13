#!/usr/bin/bash

set -e

normalization_factor=$1
input=$2
output=$3

if [ "$#" -ne 3 ]; then
  echo "  Usage: bash filter_kmers.sh normalization_factor input output " >&2 ;
  echo "Exiting now!!!"
  exit 1 ;
fi

minkmercov = 9/$normalization_factor
echo " Min k-mer coverage is " $minkmercov 

echo "  Removing likely erroneous k-mers "
awk -F "\t" -v var=$minkmercov '{if($2>var){print}}' $input > $output
