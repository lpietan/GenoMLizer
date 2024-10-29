#!/usr/bin/env python3

from setuptools import setup, find_packages, Command
import subprocess

class InstallCommand(Command):
	description = 'Install R dependencies and check bcftools'
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
        	# Check for bcftools
		try:
			subprocess.run(['bcftools', '--version'], check=True)
		except subprocess.CalledProcessError:
			print("Warning: bcftools not found. Please install bcftools manually before proceeding.")
			
        	# Install R dependencies
		try:
			subprocess.run(['Rscript', 'install.R'], check=True)
		except subprocess.CalledProcessError as e:
			print("Failed to install R dependencies. Please check R installation and try again.")
			raise e

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
	],
	cmdclass={
		'install_dependencies': InstallCommand,
	}
)

