#!/usr/bin/bash

set -e

file1=$1
file2=$2


if [ "$#" -ne 2 ]; then 
  echo "  Usage: bash script.sh file1.fq.gz file2.fq.gz" >&2 ;
  echo "Exiting now!!!"	
  exit 1 ;
fi

echo "  Counting total bases "

if [ ("${file1: -9}" == ".fastq.gz" && "${file2: -9}" == ".fastq.gz") || ("${file1: -6}" == ".fq.gz" && "${file2: -6}" == ".fq.gz") ]; then
  zcat {$file1} {$file1} | awk 'BEGIN{bases=0} {if(NR%4==2) {bases+=length($0)}} END {print bases/1e+9}' 
elif [ ("${file1: -6}" == ".fastq" && "${file2: -6}" == ".fastq") || ("${file1: -3}" == ".fq" && "${file2: -3}" == ".fq") ]; then
  cat {$file1} {$file1} | awk 'BEGIN{bases=0} {if(NR%4==2) {bases+=length($0)}} END {print bases/1e+9}'
else
  echo "  Oppsie deisy - Check file format" >&2 ;
  exit 1;
fi
  
