![Kvar logo](figures/kvar_logo.png)


### **Kvar** is a pipeline for finding low frequency kmers in genomic data associated with disease. 

## Description

The overall goal is to find low-frequency and consensus-level kmers that are associated with certain disease phenotypes. So far we have outlined a pipeline for doing this in the slides and it goes something like: 1. get kmers; 2. filter kmers (based on frequency/location); and after running on a balanced set of disease & non-disease, 3. find kmers associated with disease phenotype. As a proof of principle, the team is using cancer samples pulled from WGS from NCI-60 cell lines (329 samples) using the SRA.

![Kvar Pipeline](figures/kvar_pipeline.png)

## STEPS
* First step
- Count kmers in the dataset
- Extract kmers and normalize frequencies by sequencing throughput
* Second step
- Generate kmer distribution plots 
- Filter erroneous kmers based on the normalised distribution frequencies
* Third step
- Calculate TF-IDF (term frequency-inverse document frequency) for the filtered kmers across samples
- Using a logistic regression model to select significant kmers using the control and test datasets
- Ranking the selected kmers 
* Fourth step
- Map the significant kmers to the reference genome and create a table of positions
- Infer biological effects using VEP

## USAGE

* General Usage
```
EXAMPLE OF HOW TO USE THE FULL PIPELINE WILL GO HERE, PATIENCE IS KEY ;)
```
* Example Usage
```
EXAMPLE OF HOW TO USE THE FULL PIPELINE WILL GO HERE, PATIENCE IS KEY ;)
```

