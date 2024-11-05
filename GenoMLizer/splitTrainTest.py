#!/usr/bin/env python3

import sys
import pandas as pd
import os

def main():
	## Split
	filename = sys.argv[1]
	testFile = filename[:-4] + "_Test.csv"
	trainFile = filename[:-4] + "_Train.csv"
	ncFile = trainFile[:-4] + "_NC.csv"
	zvFile = ncFile[:-4] + "_zv.csv"
	zvFileT = zvFile[:-4] + "_T.csv"
	df = pd.read_csv(filename, dtype=object)
	df_test = df.sample(frac=0.2, replace=False, axis=1, random_state=int(sys.argv[3]))
	df_train = df.drop(list(df_test.columns), axis = 1)
	df_test.to_csv(testFile)
	df_train.to_csv(trainFile)

	# NC80
	# fail = 0.8*len(df_train.columns)
	fail = float(sys.argv[2])*len(df_train.columns)
	remove = False
	j = ','
	# dataset file
	with open(trainFile, "r") as f:
		lines = f.readlines()
	with open(ncFile, "w") as f:
		for line in lines:
			lineN = line.rstrip('\n')
			lineList = lineN.split(',')
			lineCount = lineList.count('.')
			if remove == True:
				remove = False
			elif lineCount <= fail:
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
			else:
				remove = True

	## Zero Variance
	# dataset file
	with open(ncFile, "r") as f:
		lines = f.readlines()
	with open(zvFile, "w") as f:
		for line in lines:
			lineN = line.rstrip('\n')
			lineList = lineN.split(',')
			line_set = set(lineList)
			lineSetLen = len(line_set)
			if lineSetLen > 2:
				f.write(line)

	d = pd.read_csv(zvFile,index_col=0)
	df1_transposed = d.T
	df1_transposed.to_csv(zvFileT)

	## Clean up
	os.remove(trainFile)
	os.remove(ncFile)
	os.remove(zvFile)

if __name__ == "__main__":
	main()
