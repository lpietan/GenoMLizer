#!/usr/bin/env python3

import sys
import pandas as pd
import math
import csv
import subprocess
import pkg_resources
import os

def main():
	d_train = pd.read_csv(sys.argv[1],index_col=0)
	d_var = d_train.columns.tolist()

	d = pd.read_csv(sys.argv[2],index_col=0)

	d = d.loc[d_var]
	d.to_csv("test_temp.csv")

	j = ','
	# dataset file
	with open("test_temp.csv", "r") as f:
		lines = f.readlines()
	with open("test_temp2.csv", "w") as f:
		for line in lines:
			lineN = line.rstrip('\n')
			lineList = lineN.split(',')
			lineCount = lineList.count('.')
			if lineCount > 0:
				## Change '.' to 0
				while lineCount > 0:
					index = lineList.index('.')
					lineList[index] = '0'
					lineCount -= 1
				lineFix = j.join(lineList) + '\n'
				f.write(lineFix)
			else:
				f.write(line)

	script_path = pkg_resources.resource_filename('GenoMLizer', 'geneSetup.sh')
	subprocess.run(['bash', script_path, "test_temp2.csv", check=True)

	binVar = int(sys.argv[4]) ##25000
	binThreshold = binVar + 1
	lastGeneVar = ''
	chromosomes = 'chr1'
	startPos = 1
	alleleBin = []
	CADDBin = []
	lineIndex = 0

	j = ','
	# dataset file
	if int(sys.argv[5]) == 1:
		with open(sys.argv[6], "r") as f:
			index_alt_lines = f.readlines()
			index_line = [eval(i) for i in index_alt_lines[0].split(",")]
			alt_line = [eval(i) for i in index_alt_lines[1].split(",")]
	with open("VARS_SORTED.csv", "r") as f:
		lines = f.readlines()
	with open("VARS_SORTED_geneVARS.csv", "w") as f:
		for line in lines:
			lineN = line.rstrip('\n')
			lineList = lineN.split(',')
			lineVarName = lineList[0]
			lineVarNameList = lineVarName.split(':')
			lineVarNameListGene = lineVarNameList[2]
			lineVarNameListChr = lineVarNameList[0]
			lineVarNameListPos = lineVarNameList[1]
			lineVarNameListVar = lineVarNameList[3]
			lineListNoName = lineList[1:]
			num_var_list = [eval(str(i)) for i in lineListNoName]
			## perform correction here
			if int(sys.argv[5]) == 1:
				if lineIndex in index_line:
					correctedVar = []
					if sum(num_var_list) > 0:
						altValue = [i for i in list(set(num_var_list)) if i > 0][0]
					else:
						altValue = alt_line[index_line.index(lineIndex)]
					for i in num_var_list:
						if i > 0:
							correctedVar.append(0)
						else:
							correctedVar.append(altValue)
					num_var_list = correctedVar
				lineIndex = lineIndex + 1
			if lineVarNameListGene == '':
				if lineVarNameListChr == chromosomes:
					if int(lineVarNameListPos) < binThreshold:
						if 'Allele' in lineVarNameListVar:
							alleleBin.append(num_var_list)
						else:
							CADDBin.append(num_var_list)
					elif len(alleleBin) == 0 and len(CADDBin) == 0:
						if 'Allele' in lineVarNameListVar:
							alleleBin.append(num_var_list)
						else:
							CADDBin.append(num_var_list)
						binThreshold = math.ceil(int(lineVarNameListPos)/binVar) * binVar + 1
						startPos = binThreshold - binVar
					else:
						if len(alleleBin) > 0:
							varNameAllele = chromosomes + ":" + str(startPos) + "_" + str(binThreshold - 1) + "_Allele,"
							alleleDF = pd.DataFrame(alleleBin)
							finAlleleVar = alleleDF.sum(axis = 0).tolist()
							lineFix = varNameAllele + j.join(map(str, finAlleleVar)) + '\n'
							f.write(lineFix)
							alleleBin = []
						if len(CADDBin) > 0:
							varNameCADD = chromosomes + ":" + str(startPos) + "_" + str(binThreshold - 1) + "_CADD,"
							CADDDF = pd.DataFrame(CADDBin)
							finCADDVar = CADDDF.sum(axis = 0).tolist()
							lineFix = varNameCADD + j.join(map(str, finCADDVar)) + '\n'
							f.write(lineFix)
							CADDBin = []
						if 'Allele' in lineVarNameListVar:
							alleleBin.append(num_var_list)
						else:
							CADDBin.append(num_var_list)
						binThreshold = math.ceil(int(lineVarNameListPos)/binVar) * binVar + 1
						startPos = binThreshold - binVar
				else:
					if len(alleleBin) > 0:
						varNameAllele = chromosomes + ":" + str(startPos) + "_" + str(binThreshold - 1) + "_Allele,"
						alleleDF = pd.DataFrame(alleleBin)
						finAlleleVar = alleleDF.sum(axis = 0).tolist()
						lineFix = varNameAllele + j.join(map(str, finAlleleVar)) + '\n'
						f.write(lineFix)
						alleleBin = []
					if len(CADDBin) > 0:
						varNameCADD = chromosomes + ":" + str(startPos) + "_" + str(binThreshold - 1) + "_CADD,"
						CADDDF = pd.DataFrame(CADDBin)
						finCADDVar = CADDDF.sum(axis = 0).tolist()
						lineFix = varNameCADD + j.join(map(str, finCADDVar)) + '\n'
						f.write(lineFix)
						CADDBin = []
					if 'Allele' in lineVarNameListVar:
						alleleBin.append(num_var_list)
					else:
						CADDBin.append(num_var_list)
					chromosomes = lineVarNameListChr
					binThreshold = math.ceil(int(lineVarNameListPos)/binVar) * binVar + 1
					startPos = binThreshold - binVar
			else:
				if lastGeneVar != '':
					if lineVarNameListGene == lastGeneVar:
						if 'Allele' in lineVarNameListVar:
							alleleBin.append(num_var_list)
						else:
							CADDBin.append(num_var_list)
					else:
						if len(alleleBin) > 0:
							varNameAllele = lastGeneVar + "_Allele,"
							alleleDF = pd.DataFrame(alleleBin)
							finAlleleVar = alleleDF.sum(axis = 0).tolist()
							lineFix = varNameAllele + j.join(map(str, finAlleleVar)) + '\n'
							f.write(lineFix)
							alleleBin = []
						if len(CADDBin) > 0:
							varNameCADD = lastGeneVar + "_CADD,"
							CADDDF = pd.DataFrame(CADDBin)
							finCADDVar = CADDDF.sum(axis = 0).tolist()
							lineFix = varNameCADD + j.join(map(str, finCADDVar)) + '\n'
							f.write(lineFix)
							CADDBin = []
						if 'Allele' in lineVarNameListVar:
							alleleBin.append(num_var_list)
						else:
							CADDBin.append(num_var_list)
						lastGeneVar = lineVarNameListGene
				else:
					if len(alleleBin) > 0:
						varNameAllele = chromosomes + ":" + str(startPos) + "_" + str(binThreshold - 1) + "_Allele,"
						alleleDF = pd.DataFrame(alleleBin)
						finAlleleVar = alleleDF.sum(axis = 0).tolist()
						lineFix = varNameAllele + j.join(map(str, finAlleleVar)) + '\n'
						f.write(lineFix)
						alleleBin = []
					if len(CADDBin) > 0:
						varNameCADD = chromosomes + ":" + str(startPos) + "_" + str(binThreshold - 1) + "_CADD,"
						CADDDF = pd.DataFrame(CADDBin)
						finCADDVar = CADDDF.sum(axis = 0).tolist()
						lineFix = varNameCADD + j.join(map(str, finCADDVar)) + '\n'
						f.write(lineFix)
						CADDBin = []
					if 'Allele' in lineVarNameListVar:
						alleleBin.append(num_var_list)
					else:
						CADDBin.append(num_var_list)
					lastGeneVar = lineVarNameListGene
		if len(alleleBin) > 0:
			varNameAllele = lineVarNameListGene + "_Allele,"
			alleleDF = pd.DataFrame(alleleBin)
			finAlleleVar = alleleDF.sum(axis = 0).tolist()
			lineFix = varNameAllele + j.join(map(str, finAlleleVar)) + '\n'
			f.write(lineFix)
		if len(CADDBin) > 0:
			varNameCADD = lineVarNameListGene + "_CADD,"
			CADDDF = pd.DataFrame(CADDBin)
			finCADDVar = CADDDF.sum(axis = 0).tolist()
			lineFix = varNameCADD + j.join(map(str, finCADDVar)) + '\n'
			f.write(lineFix)

	with open("VARS_SORTED_geneVARS.csv", 'r') as f1, open("gene.csv", 'a') as f2:
		f2.write(f1.read())

	d = pd.read_csv("gene.csv",index_col=0)
	df1_transposed = d.T
	df1_transposed.to_csv(sys.argv[3])

	os.remove("VARS.csv")
	os.remove("gene.csv")
	os.remove("VARS_SORTED.csv")
	os.remove("VARS_SORTED_geneVARS.csv")
	os.remove("test_temp.csv")
	os.remove("test_temp2.csv")
	print("Test set prepared successfully")

if __name__ == "__main__":
	main()







