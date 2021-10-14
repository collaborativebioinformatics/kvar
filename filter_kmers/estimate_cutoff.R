#!/usr/bin/env Rscript

args <- commandArgs(TRUE)

argsLen <- length(args)
if (argsLen != 4) stop('\n\tPlease run as : Rscript estimate_cutoff.R genome_size_mb read_length bases_throughput_mb kmer_size\n\tDont forget to check units\n\n');

genome_size_mb <- as.integer(args[1])
read_length <- as.integer(args[2])
bases_throughput_mb <- as.integer(args[3])
kmer_size <- as.integer(args[4])

#write(genome_size_mb, stderr())
#write(read_length, stderr())
#write(bases_throughput_mb, stderr())

prob_miss = 1e-6

calc_frac = 1 - (read_length / (genome_size_mb*1e+6))
needed_reads_million = log(prob_miss, base=calc_frac)

min_genome_coverage = (needed_reads_million) / (genome_size_mb)
min_kmer_coverage = ((read_length - kmer_size + 1)/read_length ) * min_genome_coverage
needed_normalized_cov = min_kmer_coverage / bases_throughput_mb
needed_normalized_cov_abs = ceiling(needed_normalized_cov)

write(needed_normalized_cov_abs, stdout())

