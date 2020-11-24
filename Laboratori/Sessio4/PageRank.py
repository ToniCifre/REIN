#!/usr/bin/python

import time
import codecs
import numpy as np
from prettytable import PrettyTable


class Edge:
    def __init__(self, origin=None, desti=None):
        self.desti = desti  # write appropriate value
        self.origin = origin  # write appropriate value
        self.weight = 1  # write appropriate value

    def __repr__(self):
        return "edge: {0} {1} {2}".format(self.origin, self.weight, self.desti)

    def __eq__(self, a):
        if isinstance(a, Edge) and isinstance(self, Edge):
            if self.origin == a.origin and self.desti == a.desti:
                return True
        return False


class Airport:
    def __init__(self, iden=None, name=None, index=None):
        self.index = index
        self.code = iden  # IATA code
        self.name = name  # airport name
        self.routes = []  # list of edges that have this airport as destination
        self.routeHash = dict()  # dict{key = airport IATA code : index in routes}
        self.outweight = 0  # write appropriate value
        self.rank = 0  # write appropriate value

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.index)

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank


airportList = []  # list of Airport
airportHash = dict()  # hash key IATA code -> Airport


def readAirports(fd):
    '''
    Reads airports from fd file and adds them into the data structures.
    '''
    print(f'Reading Airport file from {fd}')
    airportsTxt = codecs.open(fd, "r", encoding="cp1252", errors="ignore")
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5:
                raise Exception('not an IATA code')
            a.name = temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code = temp[4][1:-1]
            a.index = cont
        except Exception:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()

    print(f'There are {cont} airports with IATA code.')


def getAirport(code):
    '''
    Given an airport code returns the airport information.
    '''
    try:
        if code not in airportHash:
            raise Exception("Airport not found.")
    except Exception:
        pass
    else:
        return airportList[airportHash[code].index]


def readRoutes(fd):
    '''
    Reads routes from fd file and adds them into the airports.

    airline code, op airline code, origin airport code, op origin code,
    dest airport code, op destination airport code
    only IATA codes
    '''
    print(f'Reading Routes file from {fd}')

    f = codecs.open(fd, "r", encoding="cp1252", errors="ignore")
    n_conn = 0
    for line in f.readlines():
        _, _, origin, _, desti, _, _, _, _ = line.split(',')
        if len(origin) == 3 and len(desti) == 3:
            if desti in airportHash and origin in airportHash:
                desti = airportHash[desti]
                if origin in desti.routeHash:
                    desti.routes[desti.routeHash[origin]].weight += 1
                else:
                    desti.routes.append(Edge(origin=origin, desti=desti.code))
                    desti.routeHash[origin] = len(desti.routes) - 1

                airportHash[origin].outweight += 1
                n_conn += 1

    f.close()
    print(f'Number of connections: {n_conn}')


def computePageRanks(L=.8, maxerr=.0001):
    '''
    Iterative method for computing PageRank values.
    '''
    n_airports = len(airportList)
    P = np.ones(n_airports) / n_airports

    z = [z.index for z in airportList if len(z.routes) == 0]

    n_iter = 0
    flag = True
    while flag:
        Q = np.zeros(n_airports)
        z_sum = sum(P[z])

        for a in airportList:
            r_sum = sum(P[airportHash[r.origin].index] * r.weight / airportHash[r.origin].outweight for r in a.routes)
            Q[a.index] = L * r_sum + (1 - L + L * z_sum) / n_airports
            # Q[a.index] = Decimal(L * (suma + Decimal(z_sum) / Decimal(n_airports)) + d)

        # print(f'Sum of PageRank: {sum(Q)}')
        flag = np.sum(np.abs(Q - P)) > maxerr
        P = Q
        n_iter += 1

    return P, n_iter


def outputPageRanks():
    '''
    Print the list of (pagerank, airport name) in descending order by pagerank.
    '''
    t = PrettyTable(['N', 'Airport', 'Ranck'])
    for index, a in enumerate(sorted(airportList, reverse=True), start=1):
        t.add_row([index, a.name, a.rank])
    print(t)


def main():
    readAirports("airports.txt")
    readRoutes("routes.txt")

    time1 = time.time()
    P, n_iter = computePageRanks(0.8)
    time2 = time.time()

    for a in airportList:
        a.rank = P[a.index]

    outputPageRanks()

    print(f'Total PageRank Sum: {sum(P)}')
    print(f'Iterations: {n_iter}')
    print(f'Time of computePageRanks(): {time2 - time1}')


if __name__ == "__main__":
    main()
