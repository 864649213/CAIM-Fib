
from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Index
import argparse
import os
import codecs


def addIndex(gI):
    f = "output" + str(gI)
    ftxt = codecs.open(f, "r", encoding='iso-8859-1')
    
    text = ''
    for line in ftxt:
        text += line
    # Insert operation for a document with fields' path' and 'text'
    ldocs = []
    ldocs.append({'_op_type': 'index', '_index': f, '_type': 'document', 'path': f, 'text': text})

    # Working with ElasticSearch
    client = Elasticsearch()
    try:
        # Drop index if it exists
        ind = Index(f, using=client)
        ind.delete()
    except NotFoundError:
        pass
    # then create it
    ind.settings(number_of_shards=1)
    ind.create()

    # Bulk execution of elasticsearch operations (faster than executing all one by one)
    print('Indexing ...')
    bulk(client, ldocs)

for gI in range(0, 16):
     addIndex(gI)
