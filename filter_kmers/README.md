
# Filtering k-mers for each sample
Since the sequencing throughput for the samples is different, we would need to calculate the normalisation factor. This is estimated using the total throughput for simplicity. And based on this normalisation factor, we would filter the kmers which likely are errors or are too rare.

# Estimating the cutoff
Use the estimate cutff script for finding minimum k-mer coverage filter threshold
```
Rscript estimate_cutoff.R genome_size_mb average_read_length run_sequencing_throughput_mb kmer_size
Rscript estimate_cutoff.R 60 100 7000 31
```

