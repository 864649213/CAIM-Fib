#!/usr/bin/env python
"""
Simple module implementing LSH
"""
import numpy
import sys
import argparse
import time

__version__ = '0.2.1'
__author__ = 'marias@cs.upc.edu'


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' %
              (method.__name__, args, kw, te - ts))
        return result

    return timed


class lsh(object):
    """
    implements lsh for digits database in file 'images.npy'
    """

    def __init__(self, k, m):
        """ k is nr. of bits to hash and m is reapeats """
        # data is numpy ndarray with images
        self.data = numpy.load('images.npy')
        self.k = k
        self.m = m

        # determine length of bit representation of images
        # use conversion from natural numbers to unary code for each pixel,
        # so length of each image is imlen = pixels * maxval
        self.pixels = 64
        self.maxval = 16
        self.imlen = self.pixels * self.maxval

        # need to select k random hash functions for each repeat
        # will place these into an m x k numpy array
        numpy.random.seed(12345)
        self.hashbits = numpy.random.randint(self.imlen, size=(m, k))

        # the following stores the hashed images
        # in a python list of m dictionaries (one for each repeat)
        self.hashes = [dict() for _ in range(self.m)]

        # now, fill it out
        self.hash_all_images()

        return

    def hash_all_images(self):
        """ go through all images and store them in hash table(s) """
        # Achtung!
        # Only hashing the first 1500 images, the rest are used for testing
        for idx, im in enumerate(self.data[:1500]):
            for i in range(self.m):
                str = self.hashcode(im, i)

                # store it into the dictionary..
                # (well, the index not the whole array!)
                if str not in self.hashes[i]:
                    self.hashes[i][str] = []
                self.hashes[i][str].append(idx)
        return

    def hashcode(self, im, i):
        """ get the i'th hash code of image im (0 <= i < m)"""
        pixels = im.flatten()
        row = self.hashbits[i]
        str = ""
        for x in row:
            # get bit corresponding to x from image..
            pix = int(x) // int(self.maxval)
            num = x % self.maxval
            if num <= pixels[pix]:
                str += '1'
            else:
                str += '0'
        return str

    def candidates(self, im):
        """ given image im, return matching candidates (well, the indices) """
        res = set()
        for i in range(self.m):
            code = self.hashcode(im, i)
            if code in self.hashes[i]:
                res.update(self.hashes[i][code])
        return res

##########################################################################

def distance(im1, im2):
    pixels1 = im1.flatten()
    pixels2 = im2.flatten()
    d = sum(abs(pixels1-pixels2))
    return d

def bf_search(me, imgIndex):
    im = me.data[imgIndex]
    minDist = float('inf')
    closestImg = -1
    for i in range(0, 1500):
        d = distance(im, me.data[i])
        if (d < minDist):
            minDist = d
            closestImg = i

    return (closestImg, minDist)

def candidate_search(me, imgIndex, candidates):
    if (len(candidates) == 0):
        return None
    im = me.data[imgIndex]
    minDist = float('inf')
    closestImg = -1
    for c in candidates:
        d = distance(im, me.data[c])
        if (d < minDist):
            minDist = d
            closestImg = c
    return (closestImg, minDist)

#########################################################################

@timeit
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', default=20, type=int)
    parser.add_argument('-m', default=5, type=int)
    args = parser.parse_args()

    print("Running lsh.py with parameters k =", args.k, "and m =", args.m)

    me = lsh(args.k, args.m)

    mode = 1 # 1 = Both, 2 = LSH, 3 = Brute-force

    # show candidate neighbors for first 10 test images
    count = 0
    total = 0
    for r in range(1500, 1510):
        im = me.data[r]
        print("Image %4d:" % (r))
        if (mode == 1 or mode == 2):
            cands = me.candidates(im)
            print("there are %4d candidates" % (len(cands)))
            total += len(cands)
            count += 1
            try:
                (minDist, closestImg) = candidate_search(me, r, cands)
                print("LSH: the closest candidate is %4d, with distance %4d " % (closestImg, minDist))
            except:
                print("LSH: there are no candidates for this image")

        if (mode == 1 or mode == 3):
            (minDist, closestImg) = bf_search(me, r)
            print("Brute-force: the closest candidate is %4d, with distance %4d " % (closestImg, minDist))

        print("--------------------------------------------------------------")

    if (mode == 1 or mode == 2):
        print("The average number of candidates is ", total/count)
    return


if __name__ == "__main__":
    sys.exit(main())
