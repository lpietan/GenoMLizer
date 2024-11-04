#!/usr/bin/env python3

import sys
import pandas as pd
import math
import csv
import subprocess
import pkg_resources
import os

def main():
	d = pd.read_csv(sys.argv[1],index_col=0)
	df1_transposed = d.T
	df1_transposed.to_csv("transposed.csv")

	script_path = pkg_resources.resource_filename('GenoMLizer', 'geneSetup.sh')
	subprocess.run(['bash', script_path, "transposed.csv", check=True)

	binVar = int(sys.argv[3]) ##25000
	binThreshold = binVar + 1
	lastGeneVar = ''
	chromosomes = 'chr1'
	startPos = 1
	alleleBin = []
	CADDBin = []

	j = ','
	if sys.argv[4] == "SFC" or sys.argv[4] == "DC":
		correction_threshold = float(sys.argv[5])
		lineIndex = 0
		testSetIndex = []
		testSetAlt = []
		with open("gene.csv", "r") as f:
			head_lines = f.readlines()
		if sys.argv[4] == "SFC":
			samSize = len(head_lines[1].split(',')) - 1
			samThreshold = samSize * correction_threshold
		else:
			targets_for_correction = np.array([eval(str(i)) for i in head_lines[1].split(',')[1:]])
	else:
		pass	
	# dataset file
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
			if sys.argv[4] == "SFC":
				count = len([i for i in num_var_list if i > 0])
				if count > samThreshold:
					testSetIndex.append(lineIndex)
					correctedVar = []
					altValue = [i for i in list(set(num_var_list)) if i > 0][0]
					testSetAlt.append(altValue)
					for i in num_var_list:
						if i > 0:
							correctedVar.append(0)
						else:
							correctedVar.append(altValue)
					num_var_list = correctedVar
				lineIndex = lineIndex + 1
			elif sys.argv[4] == "DC":
				index_alt_alleles = [i for i, n in enumerate(num_var_list) if n > 0]
				num_alt_alleles_for_correction = len(index_alt_alleles)
				selected_targets_sum = np.sum(targets_for_correction[index_alt_alleles])
				ratio_alt_allele_targets = selected_targets_sum/num_alt_alleles_for_correction
				if ratio_alt_allele_targets < correction_threshold:
					testSetIndex.append(lineIndex)
					correctedVar = []
					altValue = [i for i in list(set(num_var_list)) if i > 0][0]
					testSetAlt.append(altValue)
					for i in num_var_list:
						if i > 0:
							correctedVar.append(0)
						else:
							correctedVar.append(altValue)
					num_var_list = correctedVar
				lineIndex = lineIndex + 1
			else:
				pass
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
		if sys.argv[3] == "SFC" or sys.argv[3] == "DC":
			with open("variables_corrected.csv", "w") as f2:		
				lineIndexListFix = j.join(map(str, testSetIndex)) + "\n"
				lineAltListFix = j.join(map(str, testSetAlt))
				f2.write(lineIndexListFix)
				f2.write(lineAltListFix)

	with open("VARS_SORTED_geneVARS.csv", 'r') as f1, open("gene.csv", 'a') as f2:
		f2.write(f1.read())

	d = pd.read_csv("gene.csv",index_col=0)
	df1_transposed = d.T
	df1_transposed.to_csv(sys.argv[2])

	os.remove("transposed.csv")
	os.remove("VARS.csv")
	os.remove("gene.csv")
	os.remove("VARS_SORTED.csv")
	os.remove("VARS_SORTED_geneVARS.csv")

if __name__ == "__main__":
	main()
