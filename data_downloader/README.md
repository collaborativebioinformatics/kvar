# DNANexus SRA Downloader


Takes in a accession file containing SRA ids and launch `sra_fastq_importer` to down load these SRAs

## Usage

1. Login in the DNAneuxs platform via the CLI tool using an api token
    - `dxpy login --token XXXXX`
2. To retrieve an api token go to `https://documentation.dnanexus.com/developer/api/authentication`
3. Run `launcher.py`

```
python data_downloader/launcher.py --help
usage: launcher.py [-h] --accession-file ACCESSION_FILE --dx-folder DX_FOLDER --log-file LOG_FILE

optional arguments:
  -h, --help            show this help message and exit
  --accession-file ACCESSION_FILE, -i ACCESSION_FILE
                        txt file containing SRR file, one per line.
  --dx-folder DX_FOLDER, -f DX_FOLDER
                        destination of output file on dnanexus platform
  --log-file LOG_FILE, -o LOG_FILE
                        log file
) 
```

## Installation

This is a pure python package and the requirements are found in `requirements.txt`

```bash

pip install -r dev-requirements.txt
```

## Example data

`./example/nci-60.srr.txt` - contains accession id from nci-60 of WXS data