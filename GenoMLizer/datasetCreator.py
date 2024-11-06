#!/usr/bin/env python3

## dependencies 
from vcf_parser import VCFParser
import numpy
import pandas as pd
import csv
import sys
import subprocess
import pkg_resources
import os
import GenoMLizer

def main():
	script_path = pkg_resources.resource_filename('GenoMLizer', 'dcSetup.sh')
	subprocess.run(['bash', script_path, sys.argv[1]], check=True)

	## targetFile, this file will be variable passed in from command line
	filename = sys.argv[2]
	df = pd.read_csv(filename)

	## Write samples and targets to dataset file
	sampleNamesList = df['sampleNames'].tolist()
	## !! Changed 'targets' to 'Targets' in df[].tolist()
	sampleTargetList = ['Targets'] + df['Targets'].tolist()
	j = ','
	sampleNamesStr = j.join(map(str,sampleNamesList))
	sampleTargetStr = j.join(map(str,sampleTargetList))
	datasetFile = open(sys.argv[3], 'w')
	datasetFile.write(f"{sampleNamesStr}\n")
	datasetFile.write(f"{sampleTargetStr}\n")
	datasetFile.close()

	## convert format into list and get index of symbol and CADD_PHRED
	with open('temp') as f:
		line = f.readlines()
	line = line[0]
	line = line.split(' ')
	line = line[-1]
	## CSQ Format as a list to obtain indices
	line = line.split('|')
	symbolIndex = line.index('SYMBOL')
	caddIndex = line.index('CADD_PHRED')
	variant_ClassIndex = line.index('VARIANT_CLASS')

	## vcf parser, infile will be variable thats passed in from command line
	my_parser = VCFParser(infile=sys.argv[1], split_variants=False, check_info=True)

	## iterate through variants
	for variant in my_parser:
		## for each variant get how many CSQ annotations there are (this is a list)
		variantCSQ = variant['info_dict']['CSQ']
		variantCsqLen = len(variantCSQ)
		## Dictionary with each allele annotation for CADD and gene symbol
		allCsqAnnotations = {}
		for annotation in variantCSQ:
			annotationList = annotation.split('|')
			annAllele = annotationList[0]
			## Original fix for insertions, commented out due to handling insertion also with other variant type another way (below)
			## Also potentially not fixing all insertion cases with this approach  
			#if annotationList[variant_ClassIndex] == 'insertion':
				#refAllele = variant['REF']
				#annAllele = refAllele + annAllele
			annDict = {'CADD_PHRED':annotationList[caddIndex],'SYMBOL':annotationList[symbolIndex]}
			if not annAllele in allCsqAnnotations.keys():
				allCsqAnnotations[annAllele] = annDict
		
		## Alternative alleles for variant from ALT, confirming possible annotations 	
		altAlleles = variant['ALT'].split(',')
		for altAllele in altAlleles:
			## handling '-' annotations, no annotations, and insertions with other variant types
			if not altAllele in allCsqAnnotations.keys():
				altAllele2 = altAllele[1:]
				if altAllele2 in allCsqAnnotations.keys():
					altAlleleIndex = altAlleles.index(altAllele)
					altAlleles[altAlleleIndex] = altAllele2
				## handling '*' alt alleles
				elif altAllele == '*':
					allCsqAnnotations[altAllele] = {'CADD_PHRED': '0', 'SYMBOL': ''}
				## handling '-' annotations
				elif '-' in allCsqAnnotations:
					allCsqAnnotations[altAllele] = allCsqAnnotations['-']
				else:
					allCsqAnnotations[altAllele] = {'CADD_PHRED': '0', 'SYMBOL': ''}
				

		## Feature variables will be annotated with the gene symbol from the first alt allele vep annotation
		## Name of each variable/feature in dataset, key in df dictionary
		firstSymbolAnnotation = list(allCsqAnnotations.keys())[0]
		chrom = variant['CHROM']
		pos = variant['POS']
		firstGeneSymbol = allCsqAnnotations[firstSymbolAnnotation]['SYMBOL']
		featureNameAllele1 = chrom + ':' + pos + ':' + firstGeneSymbol + ':Allele1'
		featureNameAllele2 = chrom + ':' + pos + ':' + firstGeneSymbol + ':Allele2'
		featureNameCADD1 = chrom + ':' + pos + ':' + firstGeneSymbol + ':CADD1'
		featureNameCADD2 = chrom + ':' + pos + ':' + firstGeneSymbol + ':CADD2'
		## Initialize sample lists for each feature per variant
		allele1List = []
		allele2List = []
		CADD1List = []
		CADD2List = []

		for samples in sampleNamesList:
			indivInfo = variant[samples]
			## potentially include other vcf chromosome abbreviations 
			if chrom == 'chrX' or chrom == 'chrY':
				## include this condition in above line with 'and' 
				if indivInfo[1] == ':':
					allele1List.append(indivInfo[0])
					allele2List.append('.')
					allele1 = indivInfo[0]
					allele2 = 0
				else:
					## condense this 
					allele1List.append(indivInfo[0])
					allele2List.append(indivInfo[2])
					allele1 = indivInfo[0]
					allele2 = indivInfo[2]
			else:
				allele1List.append(indivInfo[0])
				allele2List.append(indivInfo[2])
				allele1 = indivInfo[0]
				allele2 = indivInfo[2]

			#if allele1 == '.':
				#allele1 = 0

			#if allele2 == '.':
				#allele2 = 0

			#allele1 = int(allele1)
			#allele2 = int(allele2)

			if allele1 == '.':
				CADD1List.append('.')
			else:
				allele1 = int(allele1)
				if allele1 > 0:
					allele1AnnotationIndex = allele1 - 1
					caddAllele1 = allCsqAnnotations[altAlleles[allele1AnnotationIndex]]['CADD_PHRED']
					if caddAllele1 == '':
						CADD1List.append(0)
					elif caddAllele1 == '0':
						CADD1List.append(0)
					else:
						CADD1List.append(float(caddAllele1))
				else:
					CADD1List.append(0)

			if allele2 == '.':
				CADD2List.append('.')
			else:
				allele2 = int(allele2)
				if allele2 > 0:
					allele2AnnotationIndex = allele2 - 1
					caddAllele2 = allCsqAnnotations[altAlleles[allele2AnnotationIndex]]['CADD_PHRED']
					if caddAllele2 == '':
						CADD2List.append(0)
					elif caddAllele2 == '0':
						CADD2List.append(0)
					else:
						CADD2List.append(float(caddAllele2))
				else:
					CADD2List.append(0)


		allele1Feature = j.join(map(str,[featureNameAllele1] + allele1List))
		CADD1Feature = j.join(map(str,[featureNameCADD1] + CADD1List))
		allele2Feature = j.join(map(str,[featureNameAllele2] + allele2List))
		CADD2Feature = j.join(map(str,[featureNameCADD2] + CADD2List))

		with open(sys.argv[3], 'a') as dataset:
			dataset.write(f'{allele1Feature}\n')
			dataset.write(f'{CADD1Feature}\n')
			dataset.write(f'{allele2Feature}\n')
			dataset.write(f'{CADD2Feature}\n')

	os.remove("temp")

	print('Dataset complete.')
	print('datasetCreator has finished successfully.')

if __name__ == "__main__":
	main()
