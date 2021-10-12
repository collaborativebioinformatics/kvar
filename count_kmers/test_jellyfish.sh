#!/usr/bin/bash

set -e

#Assuming kmer size, genomic coverage, zipped paired end reads and output directory as inputs

kmersize=$1
nuc_cov=$2
file1=$3
file2=$4
outdir1=$5

whole_number='^[0-9]+$'

if [ "$#" -ne 5 ] || ! [[ ${nuc_cov} =~ ${whole_number} ]] || ! [[ ${kmersize} =~ ${whole_number} ]]; then
  echo "  Usage: bash test_jellyfish.sh ksize nuc_coverage file1.fq.gz file2.fq.gz /path/to/output/folder" >&2 ;
  echo "Exiting now!!!"	
  exit 1 ;
fi

if [ ! -e "${outdir}1" ]; then
  mkdir -p $outdir1 ;
fi
cd $outdir1 ;

echo "  Running Jellyfish counting "
jellyfish count -C -m $kmersize -s 100M -t $(eval nproc) <(zcat $file1) <(zcat $file2) -o mer_counts.jf

echo "  Creating histogram "
jellyfish histo -t 10 mer_counts.jf > mer_counts.histo

echo "  Dumping kmers "
jellyfish dump mer_counts.jf > mer_counts.fasta
cat mer_counts.fasta | tr "\n" "\t" | sed -e 's/\t>/\n/g' -e 's/^>//' | awk -F'\t' '{print $2"\t"$1}' >mer_counts.normalised.tsv


