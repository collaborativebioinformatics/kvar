#!/bin/bash
#
# Kvar Pipeline
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";




#######################################
# run_kmerFinding()
# uses jellyfish to find relevant kmers
# Globals:
#   None
# Arguments:
#  local fastq_1=$1; - path to the forward pairs
#  local fastq_2=$2; - path to the reverse pairs
#  local out_path=$3; - the output path
# Outputs:
#   Creates a tsv file for the kmers and associated counts.
#######################################
function run_kmerFinding() {
  # arguments
  local kmer_size=$1;
  local nuc_cov=$2;
  local fastq_1=$3;
  local fastq_2=$4;
  local out_path=$5;

  # echo "2kmer size $kmer_size" 
  # echo "2nuc coverage $nuc_cov"
  # echo "2file 1 $file_1"
  # echo "2file 2 $file_2"
  # echo "2 output directory $out_path"
  # iteratively add genomes to the multifasta
  if [[ ! -f ${out_path}_mer_counts.normalised.tsv ]]; then
    echo;echo; echo "Kvar: Running the kmer counting step."; echo;echo;
    bash ${DIR}/count_kmers/test_jellyfish.sh ${kmer_size} ${nuc_cov} ${fastq_1} ${fastq_2} ${out_path};
  else
    echo "NOT running kmer counting step... already done";
  fi
}

#######################################
# run_kmerFinding_directory()
#   performs kmer finding on a directory
# Globals:
#   None
# Arguments:
#  local fastq_1=$1; - path to the forward pairs
#  local fastq_2=$2; - path to the reverse pairs
#  local out_path=$3; - the output path
# Outputs:
#   Creates a tsv file for the kmers and associated counts.
#######################################
function run_kmerFinding_directory() {
  # arguments
  local positive_fastq_dir=$1;
  local negative_fastq_dir=$2;
  local kmer_size=$3;
  local nuc_cov=$4;
  local out_path=$5;
  # echo "1kmer size $kmer_size" 
  # echo "1nuc coverage $nuc_cov"
  # echo "1 output directory $out_path"
  # iteratively add genomes to the multifasta (POSITIVES)
  for fastq_file in $positive_fastq_dir*_1.fq.gz; do
    out_prefix=${out_path}/pos_kmer_info/"$(basename -- ${fastq_file%_1.fq.gz})";
    if [[ ! -f ${out_prefix} ]]; then
      run_kmerFinding ${kmer_size} ${nuc_cov} ${fastq_file%_1.fq.gz}_1.fq.gz ${fastq_file%_1.fq.gz}_2.fq.gz ${out_prefix};
    else
      echo "NOT running kmer counting step for ${fastq_file} already done";
    fi
  done

  # iteratively add genomes to the multifasta (NEGATIVES)
  for fastq_file in $negative_fastq_dir*_1.fq.gz; do
    out_prefix=${out_path}/neg_kmer_info/"$(basename -- ${fastq_file%_1.fq.gz})";
    if [[ ! -f ${out_prefix} ]]; then
      run_kmerFinding ${kmer_size} ${nuc_cov} ${fastq_file%_1.fq.gz}_1.fq.gz ${fastq_file%_1.fq.gz}_2.fq.gz ${out_prefix};
    else
      echo "NOT running kmer counting step for ${fastq_file} already done";
    fi
  done
}

#######################################
# run_kmerAnalysis()
# Uses TFIDF and recursive feature selection
# to find the most important kmers for differentiating
# between positive and negative samples.
# Globals:
#   None
# Arguments:
#  local pythonConfig=$1; - the path to the python config
#  local outputPrefix=$2; - an output path and prefix 
#  local kmer_cutoff=$3; - the kmer cutoff [50000 is preffered]
# Outputs:
#   Creates a fasta file for the kmers that can be used 
#   later in the pipeline for functional analysis. 
#######################################
function run_kmerAnalysis() {
  # arguments
  local pos_dir=$1;
  local neg_dir=$2;
  local outputPrefix=$3;
  local kmer_cutoff=$4;
  # iteratively add genomes to the multifasta
  if [[ ! -f ${outputPrefix}.fa ]]; then
    echo;echo; echo "Kvar: Running the kmer Analysis step.";echo;echo;
    python3 ${DIR}/kmer_analysis/kmer_selector.py --positive_file_path ${pos_dir} \
                                                  --negative_file_path ${neg_dir} \
                                                  --output ${outputPrefix} \
                                                  --kmer_cutoff ${kmer_cutoff} \
                                                  --fasta_out_path ${outputPrefix}.fa
  else
    echo "NOT running kmer Analysis step - already finished";
  fi
}

#######################################
# run_kmerMapping()
#   This function maps the kmers to a genome and finds variants
#   using the kmers. 
# Globals:
#   None
# Arguments:
#  local reference=$1 - path to reference genome
#  local kmers_fasta=$2 - path to kmers fasta
#  local gff_file=$3 - path to GFF file
#  local edit_distance=$4 - edit distance [DEFAULT 1]
#  local threads=$5 - threads [DEFAULT 4]
# Outputs:
#   Creates a fasta file for the kmers that can be used 
#   later in the pipeline for functional analysis. 
#######################################
function run_kmerMapping() {
  # arguments
  local reference=$1
  local kmers_fasta=$2
  local gff_file=$3
  local edit_distance=$4
  local threads=$5
  local output_directory=$6
  # iteratively add genomes to the multifasta
  if [[ ! -f ${output_directory}/output.vep.txt ]]; then
    echo;echo; echo "Kvar: Running the kmer mapping step.";echo;echo;
    bash ${DIR}/functional_impact/get_functional_impact.sh ${reference} \
                                                           ${kmers_fasta}\
                                                           ${gff_file}\
                                                           ${edit_distance}\
                                                           ${threads}\
                                                           ${output_directory}
  else
    echo "NOT running kmer Mapping step - already finished";
  fi
}

#######################################
# Main function runs the kvar pipeline
# Globals:
#   None
# Arguments:
#   None
# Outputs:
#   None
#######################################
function main(){
    # input arguments
    local config_file=$1
    source $config_file;
    
    # define variables
    outputPrefix="kvar_analysis"
    # make the output directory structure
    mkdir ${output_directory}
    mkdir ${output_directory}/positives/
    mkdir ${output_directory}/negatives/
    mkdir ${output_directory}/pos_kmer_info/
    mkdir ${output_directory}/neg_kmer_info/
    mkdir ${output_directory}/kmer_ranking/
    mkdir ${output_directory}/variant_finding/
    # running underlying methods
    run_kmerFinding_directory ${positive_fastq_dir} ${negative_fastq_dir} ${kmer_size} ${nuc_cov} ${output_directory}
    mv ${output_directory}/pos_kmer_info/*tsv ${output_directory}/positives/;
    mv ${output_directory}/neg_kmer_info/*tsv ${output_directory}/negatives/;
    run_kmerAnalysis ${output_directory}/positives/ ${output_directory}/negatives/ ${output_directory}/kmer_ranking/k ${kmer_cutoff}
    run_kmerMapping ${reference} ${outputPrefix}.fa ${gff_file} ${edit_distance} ${threads} ${output_directory}/variant_finding/
}

echo "Running Kvar.. ";
main $1;
echo "Kvar has finished!"