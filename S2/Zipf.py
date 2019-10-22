import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json

FILENAME = "./output.json"
RANGE = 10000 # num of words to be considered
DISCARD_UP = 1  # num of words of max range to discard (min 1 to avoid the sum)

#  [--RANGE-------]
# good values: 2000 <= range <= 15000
# we should not discard any word (=1)

def zipf(x, a, b, c):
    return c / (x + b)**a

def plot(xdata, ydata, fitLinear, xlogdata, ylogdata, fitLog):
    plt.figure(figsize=(8,4))
    plt.subplot(121)
    plt.plot(xdata, ydata, 'b-', label='Data')
    plt.plot(xdata, fitLinear, 'r-', label='Fit')
    plt.legend()
    plt.xlabel('Rank')
    plt.ylabel('Frequency')  

    plt.subplot(122)
    plt.plot(xlogdata, ylogdata, 'b-', label='Log data')
    plt.plot(xlogdata, fitLog, 'r-', label='Fit')
    plt.legend()
    plt.xlabel('Log Rank')
    plt.ylabel('Log Frequency')  
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    with open(FILENAME) as jsonFile:
        data = json.load(jsonFile)
        sortedData = sorted(data.items(), key=lambda kv: kv[1], reverse=True)
        rank = 1    
        xdata = []
        ydata = []

        for i in range(0,len(sortedData)):
            if i >= DISCARD_UP:
                word = sortedData[i]
                if rank <= RANGE:
                    xdata.append(rank)
                    ydata.append(word[1])
                    rank += 1

        xlogdata = list(np.log(xdata))
        ylogdata = list(np.log(ydata))
        
        popt, pcov = curve_fit(zipf, xdata, ydata)
        print("a: " + str(popt[0]) + " b: " + str(popt[1]) + " c: " + str(popt[2]))

        linearFit = []
        logFit = []

        for x in xdata:
            z = zipf(x,*popt)
            logz = np.log(z)
            linearFit.append(z)
            logFit.append(logz)

        plot(xdata, ydata, linearFit, xlogdata, ylogdata, logFit)
