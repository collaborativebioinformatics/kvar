# Testing
This directory contains test files (fastq) and a config file that can be used to test that kvar is working appropriately. 

0. get the needed files
```
wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_38/GRCh38.primary_assembly.genome.fa.gz;
gzip -d GRCh38.primary_assembly.genome.fa.gz;
wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_38/gencode.v38.primary_assembly.annotation.gff3.gz;
gzip -d gencode.v38.primary_assembly.annotation.gff3.gz;
```

1. Activate conda env
```
conda activate kvar
```

2. Run the tool
```
bash kvar.sh testing/kvar_test.config
```