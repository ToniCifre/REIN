#!/usr/bin/python

import time
import sys
import codecs
import numpy as np
from operator import itemgetter
import argparse


class Edge:
    def __init__ (self, origin=None, index=None):
        self.origin = ...  # write appropriate value
        self.weight = ...  # write appropriate value
        self.index = ...   # write appropriate value

    def __repr__(self):
        return "edge: {0} {1} {2}".format(self.origin, self.weight, self.index)
        
    ## write the rest of code you need for this class


class Airport:
    def __init__ (self, iden=None, name=None, index=None):
        self.code = iden     # IATA code
        self.name = name     # airport name
        self.routes = []     # list of edges that have this airport as destination
        self.routeHash = dict()  # dict{key = airport IATA code : index in routes}
        self.outweight = ...   # write appropriate value
        self.index = index

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.index)
    
    ## write the rest of code you need for this class
    

airportList = []      # list of Airport
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
        except Exception as inst:
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
            raise Exception ("Airport not found.")
    except Exception as inst:
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

    # write your code
    

def computePageRanks(G):
    '''
    Iterative method for computing PageRank values.
    '''
    # n, _ = G.shape # nombre de vertexs de G;
    # P = np.ones(n) / n
    # L = 0.8
    # flag = True
    # while flag:
    #     Q = np.ones(n) # vector de mida n ple de 0;
    #     for i in range(n):
    #         Q[i] = L * () P[j] * w(j,i) / out(j) + (1-L)/n;)
    #
    #     P = Q;

    # write your code


def outputPageRanks():
    '''
    Print the list of (pagerank, airport name) in descending order by pagerank.
    '''
    # write your code 
   

def main():
    
    readAirports("airports.txt")
    readRoutes("routes.txt")
    
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    
    print(f'#Iterations: {iterations}')
    print(f'Time of computePageRanks(): {time2 - time1}')


if __name__ == "__main__":
    main()
