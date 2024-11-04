#!/usr/bin/env python3

from setuptools import setup, find_packages
import subprocess
import sys

r_packages = [
    "MachineShop", "recipes", "readr", "doSNOW", "dplyr"
]

def install_r_dependencies():
	for package in r_packages:
		try:
			subprocess.check_call(['R', '-e', f'if(!requireNamespace("{package}", quietly=TRUE)) install.packages("{package}")'])
		except subprocess.CalledProcessError:
			print(f"Error installing R package: {package}", file=sys.stderr)
			#sys.exit(1)

def check_bcftools():
	try:
		# Check if bcftools is installed
		subprocess.run(['bcftools', '--version'], check=True)
	except subprocess.CalledProcessError:
		print("bcftools not found. Install bcftools before proceeding")

# Call to install R dependencies
install_r_dependencies()
# Check for bcftools
check_bcftools()

setup(
	name='GenoMLizer',
	version='0.1',
	description='A machine learning pipeline for prioritizing variants as genetic modifiers in rare disorders.',
	author='Lucas Pietan',
	url='https://github.com/lpietan/GenoMLizer',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'datasetCreator=GenoMLizer.datasetCreator:main',
			'split=GenoMLizer.split:main',
			'varPrep=GenoMLizer.varPrep:main',
                        'geneTransform=GenoMLizer.geneTransform:main',
                        'genePrep=GenoMLizer.genePrep:main',
			'CMI=GenoMLizer.rscripts:CMI_main',
                        'GLM=GenoMLizer.rscripts:GLM_main',
                        'DTVI=GenoMLizer.rscripts:DTVI_main',
                        'mlVar=GenoMLizer.rscripts:mlVar_main',
                        'mlGene=GenoMLizer.rscripts:mlGene_main'
		],
	},
	package_data={
        	'GenoMLizer': ['*.sh', '*.R'],
	},
	install_requires=[
		'pandas',
		'vcf_parser'
	]
)


