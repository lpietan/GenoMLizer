#!/bin/bash
tail -n +3 $1 > "VARS.csv"
head -n 2 $1 > "gene.csv"
sort --field-separator=':' -V -k 3,3 -k 1,1 -k 2,2 "VARS.csv" > "VARS_SORTED.csv"
