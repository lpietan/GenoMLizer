#!/usr/bin/env python3

import subprocess
import sys
import importlib.resources as pkg_resources
import GenoMLizer

def CMI_main():
    with pkg_resources.path(GenoMLizer, 'CMI.R') as cmi_r_path:
        subprocess.run(['Rscript', str(cmi_r_path)] + sys.argv[1:], check=True)

def GLM_main():
    with pkg_resources.path(GenoMLizer, 'GLM.R') as glm_r_path:
        subprocess.run(['Rscript', str(glm_r_path)] + sys.argv[1:], check=True)

def DTVI_main():
    with pkg_resources.path(GenoMLizer, 'DTVI.R') as dtvi_r_path:
        subprocess.run(['Rscript', str(dtvi_r_path)] + sys.argv[1:], check=True)

def mlVar_main():
    with pkg_resources.path(GenoMLizer, 'mlVar.R') as mlVar_r_path:
        subprocess.run(['Rscript', str(mlVar_r_path)] + sys.argv[1:], check=True)

def mlGene_main():
    with pkg_resources.path(GenoMLizer, 'mlGene.R') as mlGene_r_path:
        subprocess.run(['Rscript', str(mlGene_r_path)] + sys.argv[1:], check=True)
