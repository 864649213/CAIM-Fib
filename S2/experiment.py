 
import TFIDFViewerAuxExperiment as t
import random
import numpy as np
import os


paths = [r"D:\Documents\_FIB_\4 FIB\CAIM\LAB\S1\arxiv",
         r"D:\Documents\_FIB_\4 FIB\CAIM\LAB\S1\20_newsgroups",
         r"D:\Documents\_FIB_\4 FIB\CAIM\LAB\S1\novels"
        ]  
index = ["arxiv", "news", "novels"]
nfiles = 20


def generate_files_list(path):
    """
    Generates a list of all the files inside a path
    :param path:
    :return:
    """
    if path[-1] == '/':
        path = path[:-1]

    lfiles = []

    for lf in os.walk(path):
        if lf[2]:
            for f in lf[2]:
                lfiles.append(lf[0] + '/' + f)
    return lfiles        


if __name__ == '__main__':
    for x in range(10):
        i = 0
        res = {}
        for path in paths:
            files = generate_files_list(path)
            files = list(np.random.choice(files, nfiles, replace=False))         
            sum = 0
            for j in range(0,nfiles,2):
                path1 = files[j]
                path2 = files[j+1]
                sim = t.experiment(index[i], [path1, path2])
                sum += sim
            res[index[i]] = sum/(nfiles/2)
            i += 1

        print(res)
