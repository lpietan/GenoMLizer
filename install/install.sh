#!/bin/bash

Rscript install.R

pip install git+https://github.com/lpietan/GenoMLizer.git

echo "Checking for bcftools dependency..."
if ! command -v bcftools &> /dev/null
then
    echo "Warning: bcftools is not installed. Please install it before proceeding."
    exit 1
else
    echo "bcftools is installed."
fi

echo "Installation of GenoMLizer and all dependancies complete."
