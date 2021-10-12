
version development

task fastp {
  input {
    File in_fastq_r1
    File in_fastq_r2

  }

  String out_fastq_r1 = basename(in_fastq_r1, '.fastq.gz') + ".trimmed.fastq.gz"
  String out_fastq_r2 = basename(in_fastq_r2, '.fastq.gz') + ".trimmed.fastq.gz"

  command <<<
    fastp -i "~{in_fastq_r1}" -I "~{in_fastq_r2}" \
      -o "~{out_fastq_r1}" -O "~{out_fastq_r2}"
  >>>

  output {
    File out_trimmed_fastq_r1 = out_fastq_r1
    File out_trimmed_fastq_r2 = out_fastq_r2
  }

  runtime {
     dx_instance_type: "mem1_ssd2_x8"
     docker: "bromberglab/fastp"
  }
}


task kmer_count {
  input {
    File in_fastq_r1
    File in_fastq_r2
    Int kmer_size
  }

  String sample_name = basename(in_fastq_r1, '_1.trimmed.fastq.gz')
  String out_fasta = sample_name + '.mer_counts.fasta'
  String out_jellyfish = sample_name + '.jf'
  String out_histogram = sample_name + '.mer_counts.histo'

  command <<<

    set -exo pipefail
    echo "Running Jellyfish counting"


    jellyfish count -F 2  <(zcat ~{in_fastq_r1}) <(zcat ~{in_fastq_r2}) \
      -m ~{kmer_size} -s 100M \
      -t  16 \
      -o "~{out_jellyfish}"


    echo "  Creating histogram "
    jellyfish histo -t 16 "~{out_jellyfish}" > "~{out_histogram}"

    echo "  Dumping kmers "
    jellyfish dump "~{out_jellyfish}" > "~{out_fasta}"

  >>>

  output {
    File out_kmer_fasta = out_fasta
    File out_jellyfish_file = out_jellyfish
    File out_histogram_file = out_histogram
  }

  runtime {
     dx_instance_type: "mem3_ssd1_x16"
     docker: "quay.io/biocontainers/jellyfish:2.2.10--h6bb024c_1"
  }
}


task calculate_normalized_kmer_counts {
  input {
    File in_fastq_r1
    File in_fastq_r2
    File kmer_fasta
  }

  String sample_name = basename(kmer_fasta, '.mer_counts.fasta')
  String out_counts = sample_name + '.mer_counts.tsv'

  command <<<
    set -exo pipefail
    nuc_cov=$(zcat ~{in_fastq_r1} ~{in_fastq_r2} | awk 'BEGIN{bases=0;} {if(NR%4==2) {bases+=length($0)}} END {print bases/1e+9}')

    paste - - < ~{kmer_fasta} \
      | sed -e 's/^>//' \
      | awk -F'\t' -v nuc_cov=$nuc_cov '{print $2"\t"$1/nuc_cov}' \
      | sort -k2,2n  > ~{out_counts}

  >>>
  output {
    File out_counts_file = out_counts
  }

  runtime {
    docker: "ubuntu:latest"
    dx_instance_type: "mem1_ssd2_x4"
  }
}