import matplotlib.pyplot as plt
import networkx as nx
import tweepy
import sys
import csv
from os import listdir
import pprint


GraphData={}
Bridges=[]

def Analyze(G):
   # GraphData['Has Bridges?'] = nx.has_bridges(G)
    GraphData['Number of Nodes'] = nx.number_of_nodes(G)
    GraphData['Number of Edges'] = nx.number_of_edges(G)
  
  #  addBridges(G)
    logtoFile()


def addBridges(G):
    bridgeList  = list(nx.bridges(G))
    with open("./output/bridges.txt", "a") as output:
        output.write(str(bridgeList))  

def logtoFile():
    w = csv.writer(open("./output/GeneralData.csv", "a"))
    for key, val in GraphData.items():
        w.writerow([key, val])