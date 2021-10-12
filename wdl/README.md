
# WDL Workflow for Kvar


## Running on dnanexus

Requirements

1. Download dxWDL

```bash
wget https://github.com/dnanexus/dxWDL/releases/download/v1.50/dxWDL-v1.50.jar 

```

## Compilation 

Workflow and tasks are compiled to project defined in Makefile

```bash
# workflow

make compile-workflow

# tasks (applets only)
make compile-tasks

```

## To launch workflow on folder of SRR fastqs

Use scripts/wf_launcher.py

```bash
 python scripts/wf_launcher.py --input_folder=/data/PRJNA523380/WXS/ --output_folder=/wdl/test/wf/ --out_log=log.json


```