#!/bin/bash
bcftools view -h $1 | grep 'CSQ' > temp
