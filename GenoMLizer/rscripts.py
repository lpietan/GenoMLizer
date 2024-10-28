#!/usr/bin/env python3

import subprocess
import sys

def CMI_main():
    subprocess.run(['Rscript', 'GenoMLizer/CMI.R'] + sys.argv[1:], check=True)

def GLM_main():
    subprocess.run(['Rscript', 'GenoMLizer/GLM.R'] + sys.argv[1:], check=True)

def DTVI_main():
    subprocess.run(['Rscript', 'GenoMLizer/DTVI.R'] + sys.argv[1:], check=True)

def mlVar_main():
    subprocess.run(['Rscript', 'GenoMLizer/mlVar.R'] + sys.argv[1:], check=True)

def mlGene_main():
    subprocess.run(['Rscript', 'GenoMLizer/mlGene.R'] + sys.argv[1:], check=True)
