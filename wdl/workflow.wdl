
version development

import 'tasks.wdl' as tasks

workflow trim_and_count {

  input {
    File in_fastq_r1
    File in_fastq_r2
    Int kmer_size
  }

  call tasks.fastp as fastp {
    input: in_fastq_r1=in_fastq_r1, in_fastq_r2=in_fastq_r2
  }

  call tasks.kmer_count as kmer_count {
    input: in_fastq_r1=fastp.out_trimmed_fastq_r1, in_fastq_r2=fastp.out_trimmed_fastq_r2, kmer_size=kmer_size
  }

  call tasks.calculate_normalized_kmer_counts as calculate_normalized_kmer_counts {
    input: in_fastq_r1=fastp.out_trimmed_fastq_r1, in_fastq_r2=fastp.out_trimmed_fastq_r2, kmer_fasta=kmer_count.out_kmer_fasta
  }

  output {
    File out_fastq_r1 = fastp.out_trimmed_fastq_r1
    File out_fastq_r2 = fastp.out_trimmed_fastq_r2
    File out_kmer_fasta = kmer_count.out_kmer_fasta
    File out_jellyfish_file = kmer_count.out_jellyfish_file
    File out_histogram_file = kmer_count.out_histogram_file
    File out_counts_file = calculate_normalized_kmer_counts.out_counts_file
  }
}