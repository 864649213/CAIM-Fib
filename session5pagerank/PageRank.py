#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None):
        self.origin = origin
        self.weight = 1 # When we initialize this instance, obviously now it has 1 edge

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)

    def incWeight(self):
        self.weight += 1

    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None, index=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0.0
        self.index = index

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

    def addIncomingEdge(self, incomingAirport):
        if not incomingAirport in self.routeHash:
            e = Edge(incomingAirport)
            self.routeHash[incomingAirport] = e
        else:
            e = self.routeHash[incomingAirport]
            e.incWeight()
            
        airportHash[e.origin].outweight += 1

        

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
Res = []

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
            a.index = cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print("There were {0} Airports with IATA code".format(cont))


def readRoutes(fd):
    print("Reading Routes file from {0}".format(fd))
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')
            originCode = temp[2]
            destCode = temp[4]
            if destCode in airportHash and originCode in airportHash:
                # for an edge (i.j), to compute pagerank we are only interested in which are the incoming edges for an airport
                destAirport = airportHash[destCode]
                destAirport.addIncomingEdge(originCode)
            else:
                raise Exception('inexistent Airports')

        except Exception as inst:
            pass
        else:
            cont += 1
            # We dont need it => less memory
            # EdgeList.append(e)
            # EdgeHash[origin + " - " + dest] = e
    routesTxt.close()
    print("There were {0} Edges with both IATA code".format(cont))

def computePageRanks():
    # Two strategies: set number of iterations or by toleration
    its = 5
    L = 0.85
    n = len(airportHash)
    P = [1/n]*n
    it = 0
    while (it < its):
        Q = [0.0]*n
        for i in range(n):
            a = airportList[i]
            sumPR = 0
            for k,v in a.routeHash.items():
                sumPR += P[airportHash[k].index] * v.weight / airportHash[k].outweight
            Q[i] = L * sumPR + (1-L)/n
        P = Q
        print(sum(i for i in P))
        it += 1
 
    for x in P:
        Res.append(x)
        
    return its


def outputPageRanks():
    for x in Res:
        print(x)
    

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    #outputPageRanks()
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)


if __name__ == "__main__":
    sys.exit(main())
