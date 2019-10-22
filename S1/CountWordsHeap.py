"""
.. module:: CountWords

CountWords
*************

:Description: CountWords

    Generates a list with the counts and the words in the 'text' field of the documents in an index

:Authors: bejar
    

:Version: 

:Created on: 04/07/2017 11:58 

"""

from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError
from elasticsearch_dsl import Index

import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit

import codecs

import argparse

__author__ = 'bejar'

if __name__ == '__main__':
    axisX = []
    axisY = []
    for gI in range(0, 16):
        index = "output" + str(gI)
        #addIndex(gI)

        try:
            client = Elasticsearch()
            voc = {}
            sc = scan(client, index=index, query={"query" : {"match_all": {}}})
            for s in sc:
                try:
                    tv = client.termvectors(index=index, id=s['_id'], fields=['text'])
                    if 'text' in tv['term_vectors']:
                        for t in tv['term_vectors']['text']['terms']:
                            if t in voc:
                                voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                            else:
                                voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
                except TransportError:
                    pass
            lpal = []

            for v in voc:
                lpal.append((v.encode("utf-8", "ignore"), voc[v]))

            N = 0;
            for pal, cnt in sorted(lpal, key=lambda x: x[0 if False else 1]):
                N = N + int(cnt)
            print(N)
            axisX.append(N)
            #print('--------------------')
            #print(f'{len(lpal)} Words')
            axisY.append(len(lpal))
        except NotFoundError:
            print(f'Index {index} does not exists')
            
            
    def HeapFunction(x, k, b):
        return k*(x**b)
    
    popt, pcov = curve_fit(HeapFunction, axisX, axisY, bounds=([0.0, 0.1],[1000000.0, 2.0]))
    
    plt.plot(axisX, axisY,"r", label="data")
    plt.plot(axisX, HeapFunction(axisX, *popt), "b--", label="fit")
    plt.ylabel("different words")
    plt.xlabel("words")
        
    print(popt)
    plt.show()
