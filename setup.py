#!/usr/bin/env python3

from setuptools import setup, find_packages
import subprocess

def install_r_dependencies():
	try:
		subprocess.run(['Rscript', 'install.R'], check=True)
	except subprocess.CalledProcessError as e:
		print("Failed to install R dependencies. Please check R installation and try again.")
		raise e

def check_bcftools():
	try:
		# Check if bcftools is installed
		subprocess.run(['bcftools', '--version'], check=True)
	except subprocess.CalledProcessError:
		print("bcftools not found. Install bcftools before proceeding")



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
	install_requires=[
		'pandas',
	],
)

# Call to install R dependencies after Python dependencies
install_r_dependencies()
check_bcftools()
