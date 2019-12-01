"""
.. module:: MRKmeansDef

MRKmeansDef
*************

:Description: MRKmeansDef



:Authors: bejar


:Version:

:Created on: 17/07/2017 7:42

"""

from mrjob.job import MRJob
from mrjob.step import MRStep

__author__ = 'bejar'


class MRKmeansStep(MRJob):
    prototypes = {}

    def jaccard(self, prot, doc):
        """
        Compute here the Jaccard similarity between  a prototype and a document
        prot should be a list of pairs (word, probability)
        doc should be a list of words
        Words must be alphabeticaly ordered

        The result should be always a value in the range [0,1]
        """


        """
        # jacc(d1,d2) = inters(d1,d2) / union(d1,d2)
        intersection = 0
        i = 0
        j = 0
        while (i < len(prot) and j < len(doc)):
            if (prot[i][0] < doc[j]):
                i += 1
            elif (prot[i][0] > doc[j]):
                j += 1
            else:
                intersection += 1
                i += 1
                j += 1

        union = len(prot) + len(doc) - intersection
        return float(intersection)/float(union)
        """


        intersection = 0
        i = 0
        j = 0
        while (i < len(prot) and j < len(doc)):
            if (prot[i][0] < doc[j]):
                i += 1
            elif (prot[i][0] > doc[j]):
                j += 1
            else:
                intersection += prot[i][1]
                i += 1
                j += 1

        union = 0
        for k,v in prot:
            union += v*v
        for v in doc:
            union += v*v
        union = union - intersection

        return float(intersection)/float(union)



    def configure_args(self):
        """
        Additional configuration flag to get the prototypes files

        :return:
        """
        super(MRKmeansStep, self).configure_args()
        self.add_file_arg('--prot')

    def load_data(self):
        """
        Loads the current cluster prototypes

        :return:
        """
        f = open(self.options.prot, 'r')
        for line in f:
            cluster, words = line.split(':')
            cp = []
            for word in words.split():
                cp.append((word.split('+')[0], float(word.split('+')[1])))
            self.prototypes[cluster] = cp

    def assign_prototype(self, _, line):
        """
        This is the mapper it should compute the closest prototype to a document

        Words should be sorted alphabetically in the prototypes and the documents

        This function has to return at list of pairs (prototype_id, document words)

        You can add also more elements to the value element, for example the document_id
        """

        # Each line is a string docid:wor1 word2 ... wordn
        doc, words = line.split(':')
        lwords = words.split()
        # Compute map here
        assignedProt = next(iter(self.prototypes))
        minDist = jaccard(self.prototypes[assignedProt], lwords)

        for k,v in self.prototypes:
            dist = jaccard(v, lwords)
            if (dist < minDist):
                minDist = dist
                assignedProt = key


        # Return pair key, value
        yield assignedProt, (doc,lwords)

    def aggregate_prototype(self, key, values):
        """
        input is cluster and all the documents it has assigned
        Outputs should be at least a pair (cluster, new prototype)

        It should receive a list with all the words of the documents assigned for a cluster

        The value for each word has to be the frequency of the word divided by the number
        of documents assigned to the cluster

        Words are ordered alphabetically but you will have to use an efficient structure to
        compute the frequency of each word

        :param key:
        :param values:
        :return:
        """
        n = 0
        clusterDocs = []
        protoMap = dict()

        for doc in values:
            n += 1
            clusterDocs.append(doc[0])
            for token in doc[1]:
                if token in protoMap:
                    protoMap[token] += 1
                else:
                    protoMap[token] = 1

        # List of pairs (term, freq)
        protoList = []
        for k,v in protoMap:
            protoList.append(k, float(protoMap[k])/float(n))

        yield key, protoList

    def steps(self):
        return [MRStep(mapper_init=self.load_data, mapper=self.assign_prototype,
                       reducer=self.aggregate_prototype)
            ]


if __name__ == '__main__':
    MRKmeansStep.run()
