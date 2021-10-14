#!/usr/bin/bash

set -e

reference=$1
kmers_seq=$2
gff_file=$3
edit_distance=$4
threads=$5
output_directory=$6

if [ "$#" -ne 3 ]; then
  echo "Usage: bash get_functional_impact.sh reference.fa kmers.fa annotation.gff edit_distance threads " >&2 ;
  echo "Exiting now!!!"
  exit 1 ;
fi


# Indexing human reference
mrsfast --index ${reference} -e ${edit_distance}

# Mapping k-mers
mrsfast --search ${reference} --seq ${kmers_seq} --threads ${threads} -o mappings.sam

# Calling variants
freebayes -f ${reference} --min-alternate-count 1 mappings.sam > output.vcf

# Functional impact wit VEP
# GFF file must have index .tbi
vep -i output.vcf -o output.vep.txt --gff ${gff_file} --fasta ${reference}
