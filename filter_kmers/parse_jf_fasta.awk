#!/usr/bin/awk -f

BEGIN {
   OFS = "\t";
}

{ 
  if ( $0 ~ "^>" ) {
      count = substr($0,2)
  } else if ( $0 !~ "^>" ) {
      sequence = $0
      print sequence, count
  }
}

