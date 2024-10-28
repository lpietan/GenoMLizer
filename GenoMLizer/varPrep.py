#!/usr/bin/env python3

import sys
import pandas as pd
import subprocess
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

	d = pd.read_csv("test_temp2.csv",index_col=0)
	df1_transposed = d.T
	df1_transposed.to_csv(sys.argv[3])

	os.remove("test_temp.csv")
	os.remove("test_temp2.csv")
	print("Test set prepared successfully")

if __name__ == "__main__":
	main()
