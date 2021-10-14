#!/usr/bin/bash
set -e

#Assuming kmer size, genomic coverage, zipped paired end reads and output directory as inputs

kmersize=$1
nuc_cov=$2
file1=$3
file2=$4
outdir1=$5

echo "kmer size: $kmersize" 
echo "nuc coverage: $nuc_cov"
echo "file 1: $file1"
echo "file 2: $file2"
echo "output directory: $outdir1"

whole_number='^[0-9]+$'

if [ "$#" -ne 5 ] || ! [[ ${nuc_cov} =~ ${whole_number} ]] || ! [[ ${kmersize} =~ ${whole_number} ]]; then
  echo "  Usage: bash test_jellyfish.sh ksize nuc_coverage file1.fq.gz file2.fq.gz /path/to/output/folder" >&2 ;
  echo "Exiting now!!!"	
  exit 1 ;
fi

echo "  Running Jellyfish counting "
jellyfish count -C -m $kmersize -s 100M -t $(eval nproc) <(gzcat $file1) <(gzcat $file2) -o ${outdir1}_mer_counts.jf

echo "  Creating histogram "
jellyfish histo -t 10 ${outdir1}_mer_counts.jf > ${outdir1}_mer_counts.histo

echo "  Dumping kmers "
jellyfish dump ${outdir1}_mer_counts.jf > ${outdir1}_mer_counts.fasta
cat ${outdir1}_mer_counts.fasta | paste - - | sed -e 's/^>//' | awk -F '\t' '{print $2"\t"$1}' | sort -k2,2nr > ${outdir1}_mer_counts.normalised.tsv
#cat mer_counts.fasta | tr "\n" "\t" | sed -e 's/\t>/\n/g' -e 's/^>//' | awk -F'\t' '{print $2"\t"$1}' >mer_counts.normalised.tsv