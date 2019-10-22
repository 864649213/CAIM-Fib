import csv
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--countFile', default=None, required=True, help='Count Words File')
parser.add_argument('--log', action='store_true', default=False, help='Print the graphics appling the logarithm')
args = parser.parse_args()

countFile = args.countFile

values = []

def isWord(w):
	for c in w:
		if(not c.isalpha()):
			return False
	return True

with open(countFile) as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	for row in readCSV:
		if(row[0] == "--------------------"):
			break
		elif(isWord(row[1][1:])):
			values.append(int(row[0]))

def f(v):
	return math.log(v,2)

def ZipFunc(x, a, b, c):
	return c/((x+b)**a)


values.reverse()
values = values[: 500]
xList = [(x+1) for x in range(len(values))]
popt, pcov = curve_fit(ZipFunc, xList, values, bounds=([0.2, -100000.0, -100000.0],[1.8, 100000.0, 1000000.0]))

newV = list(map(f, values))
nXList = list(map(f, xList))
if (args.log):
    plt.plot(nXList, newV, "r", label="data")
    plt.plot(list(map(f, xList)), list(map(f,ZipFunc(xList, *popt))), "b--", label="fit")
    plt.ylabel("log(frequency)")
    plt.xlabel("log(rank)")
else:
    plt.plot(xList, values,"r", label="data")
    plt.plot(xList, ZipFunc(xList, *popt), "b--", label="fit")
    plt.ylabel("frequency")
    plt.xlabel("rank")

print(popt)
plt.show()


