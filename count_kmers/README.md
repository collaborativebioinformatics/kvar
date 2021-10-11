### Kmer counting from Illumina SR data, post adaptor trimming
1) Use a easy to use kmer tool with k=21 (Jellyfish2 or Meryl)
2) Generate kmer frequency table, and kmers list with frequencies - per sample
3) Calculate the kmer coverage per sample : kcov = (L-k+1)/L * C
 where L is read length, k is kmer size, C is coverage per nucleotide
 Ex : k=21, L=100 then kcov = 0.88 * C
4) Normalise the kmer frequencies by their average sample kmer coverage

## USAGE
* General
```
bash test_jellyfish.sh ksize nuc_coverage file1.fq.gz file2.fq.gz /path/to/output/folder
```
* Example
```
bash test_jellyfish.sh 12 25 cancer_reads_1.fq.gz cancer_reads_2.fq.gz ./output
```
