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
PR = []

L = 0.85
tol = 10**(-10)

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
    routesTxt.close()
    print("There were {0} Edges with both IATA code".format(cont))

def computePageRanks():
    n = len(airportHash)
    P = [1/n]*n
    # Disconnected nodes PR calculation
    discN = len(list(filter(lambda a: a.outweight == 0.0, airportList)))
    disconnectedPRfixed = (L/float(n-1))*discN  # outweight = n-1, so L/(n-1), and this for all discN nodes
    disconnectPRvariable = 1/n  # All values in P at the first iteration are 1/n
    ######## ------------------------------------------------------------------------------------- ########
    stop = False
    its = 0
    while (not stop):
        Q = [0.0]*n
        for i in range(n):
            a = airportList[i]
            totalDiscPR = disconnectedPRfixed*disconnectPRvariable
            sumPR = 0
            for k,v in a.routeHash.items():
                sumPR += P[airportHash[k].index] * v.weight / airportHash[k].outweight
            Q[i] = L * sumPR + (1-L)/n + totalDiscPR
        stop = checkDifference(tol, P, Q)
        P = Q
        disconnectPRvariable = (1-L)/n + totalDiscPR
        #print(sum(i for i in P))    # Check that at each iteration, P sums 1
        its += 1

    global PR
    PR = P.copy()

    return its

def checkDifference(tol, P, Q):
    for x, y in zip(P,Q):
        if (abs(x-y) > tol):
            return False
    return True

def outputPageRanks():
    L = []
    i = 0
    for k in airportHash:
        a = airportHash[k]
        x = (a.name, PR[i])
        L.append(x)
        i += 1
    L.sort(key = lambda x: x[1], reverse = True)
    print("#### (Airport Name, PR) ####")
    for (x,y) in L:
        print("(%s, %s)"%(x, y))



def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print("#Iterations:", iterations, ", with", tol, "Tolerance between iterations")
    print("Time of computePageRanks():", time2-time1)


if __name__ == "__main__":
    sys.exit(main())
