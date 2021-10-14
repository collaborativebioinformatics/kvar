![Kvar logo](figures/kvar_logo.png)

### **Kvar** is a pipeline for finding kmers in genomic data associated with disease. 

# Using Kvar

## dependencies
* dont worry bout it - use the following with conda:
```
conda env create -f kvar.yml
```

## General Usage
```
bash kvar.sh kvar.config
```

## Setting up the config file.
The only thing that needs set up is the config file. From here, everything else is completely automated.

The config file requires information about the directories storing fastqs for the **positive** samples, and a directory for the **negative** samples. The positive and negative just refere to the fact that kvar finds kmers that allow for differentiating to sets of fastq files (for example, primary vs metastatic cancer). The directory structure for the input typically looks as follows:

```
kvar_example_out_dir/
├── kvar.config
├── negative_fastqs (DIRECTORY WITH FASTQ FILES, unzipped)
│   ├── neg_fastq_1_1.fastq
│   ├── neg_fastq_1_2.fastq
│   ├── neg_fastq_2_1.fastq
│   └── neg_fastq_2_2.fastq
├── positive_fastqs (DIRECTORY WITH FASTQ FILES, unzipped)
│   ├── pos_fastq_1_1.fastq
│   ├── pos_fastq_1_2.fastq
│   ├── pos_fastq_2_1.fastq
│   └── pos_fastq_2_2.fastq
├── reference_genome.fa
└── reference_genome.gff3
```

With that set (congrats! we're almost there),  set up the `kvar.config` as follows:

```
## CHANGE THE FOLLOWING.
positive_fastq_dir=/global/path/kvar_example_out_dir/positive_fastqs/
negative_fastq_dir=/global/path/kvar_example_out_dir/negative_fastqs/
reference=GRCh38_latest_genomic.fna # more info below
gff_file=gencode.v38.primary_assembly.annotation.gff3 # more info below
output_directory=./output_directory

## BELOW CAN BE LEFT AS IS. (i.e. dont change, why make life hard?)
edit_distance=1 #DEFAULT
threads=4 #DEFAULT - threads being used on compute.
kmer_size=31 #DEFAULT - kmer size used during analysis.
nuc_cov=25 #DEFAULT - this is the coverage used for finding kmers.
kmer_cutoff=50000 #DEFAULT - this is the total number of kmers to select from.
```

The only thing not discussed is obtaining a reference genome and associated gff3 file. We assume the user can find these online, but we give commands for obtaining the human reference and gff3 below. With all of that said, run the command above (i.e. `bash kvar.sh kvar.config`).

## Obtaining Data (reference genome and associated gff3 file)
The pipeline requires a reference genome and gff3 file (as seen in the config file). If you're working with, for example, tomatoes, then these files can be found online. If you're working with human samples, then the below commands will download the required data. 

* obtain the primary human genome.
```
wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_38/GRCh38.primary_assembly.genome.fa.gz
```
* obtain the gff32 file
```
wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_38/gencode.v38.primary_assembly.annotation.gff3.gz
```

# More information on Kvar

## Description

The overall goal is to find low-frequency and consensus-level kmers that are associated with certain disease phenotypes. So far we have outlined a pipeline for doing this in the slides and it goes something like: (1) get kmers (2) filter kmers (based on frequency/location) and after running on a balanced set of disease & non-disease (3) find kmers associated with disease phenotype (4) identify probable biological effects. As a proof of principle, the team is using cancer samples pulled from WGS from NCI-60 cell lines (329 samples) using the SRA.

![Kvar Pipeline](figures/kvar_pipeline.png)

## Introduction

Identifying k-mers—substrings of length _k_—is a common bioinformatics technique, including applications in genome and transcriptome assembly, error correction of sequencing reads, and taxonomic classification of metagenomes. More recently, k-mers have been used for genotyping of structural variations in large datasets in a mapping-free manner. 

Sample comparison based on k-mers profiles provides a computationally efficient mapping-free way to address key differences between two biological conditions, avoiding the limitations of mappability and errors in the reference genome. Of particular interest are case-control studies, that allow to pinpoint genetic loci putatively implicated with a phenotype or a disease.

Here we develop a pipeline that takes as input samples sequencing data from to two conditions, and compares their k-mer profiles, highlighting k-mers that are relevant to distinguish between the datasets. We used this approach in a panel of cancer cell lines NCI-60 comparing between primary versus metastatic tissue to highlight mutational signatures underlying cancer progression.

## Methods

**Dataset description.** As a proof of concept, we used whole exome sequencing (WES) of the NCI-60 dataset, a panel of 60 different human tumor cell lines widely used for the screening of compounds to detect potential anticancer activity.

**K-mer counting and filtering.** K-mer frequencies were obtained for each sample, using the tool Jellyfish. First, counts of k-mers of size 31 were obtained with `jellyfish count` . Using a custom script, k-mers sequence and counts were tabulated to facilitate downstream analyses. The frequency distribution were plotted using R, and low frequency k-mers likely arising from sequencing errors were removed.

**Relevant k-mers selection.** Measure the relevance of k-mers to the condition using TF-IDF (term frequency-inverse document frequency) using pre-defined control and test datasets. K-mers significantly correlated too the disease are extracted using logistic regression followed by ranking and/or classification of the significant k-mers.

**Inferring probable biological effects.** The genomic positions of the disease associated k-mers are identified and these positions are run through the ensembl-VEP pipeline to detect probable biological consequences. 

## Workflow
### I step
- Count kmers in the dataset
- Extract kmers and normalize frequencies by sequencing throughput
### II step
- Generate kmer distribution plots
- Filter erroneous kmers based on the normalised distribution frequencies
### III step
- Calculate TF-IDF for the filtered kmers across samples
- Using a logistic regression model to select significant kmers using the control and test datasets
- Ranking the selected kmers
### IV step
- Map the significant kmers to the reference genome and create a table of positions
- Infer biological effects using VEP

