#!/usr/bin/env python3

import subprocess
import sys
import psutil
import GenoMLizer

def get_default_ppsize():
    """Calculate default ppsize based on system memory"""
    memory_gb = psutil.virtual_memory().total / (1024**3)
    if memory_gb <= 8:
        return 100000
    elif memory_gb <= 16:
        return 200000
    elif memory_gb <= 32:
        return 300000
    else:
        return 500000

def run_rscript(script_name, args, ppsize=None):
    """Generic R script runner with configurable ppsize"""
    cmd = ['Rscript']
    if ppsize:
        cmd.extend(['--max-ppsize', str(ppsize)])
    cmd.extend([f'GenoMLizer/{script_name}'] + args)
    subprocess.run(cmd, check=True)

def CMI_main():
    # Get ppsize from environment variable or use default
    ppsize = int(os.environ.get('GENOMLIZER_PPSIZE', get_default_ppsize()))
    run_rscript('CMI.R', sys.argv[1:], ppsize=ppsize)

def GLM_main():
    ppsize = int(os.environ.get('GENOMLIZER_PPSIZE', get_default_ppsize()))
    run_rscript('GLM.R', sys.argv[1:], ppsize=ppsize)

def DTVI_main():
    ppsize = int(os.environ.get('GENOMLIZER_PPSIZE', get_default_ppsize()))
    run_rscript('DTVI.R', sys.argv[1:], ppsize=ppsize)

def mlVar_main():
    ppsize = int(os.environ.get('GENOMLIZER_PPSIZE', get_default_ppsize()))
    run_rscript('mlVar.R', sys.argv[1:], ppsize=ppsize)

def mlGene_main():
    ppsize = int(os.environ.get('GENOMLIZER_PPSIZE', get_default_ppsize()))
    run_rscript('mlGene.R', sys.argv[1:], ppsize=ppsize)
