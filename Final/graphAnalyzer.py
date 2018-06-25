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
    GraphData['Has Bridges?'] = nx.has_bridges(G)
    addBridges(G)
    logtoFile()


def addBridges(G):
    filetoWrite = open("./output/bridges.txt",'a')
    bridgeList  = list(nx.bridges(G))
    with open("./output/bridges.txt", "a") as output:
        output.write(str(bridgeList))  

def logtoFile():
    w = csv.writer(open("./output/GeneralData.csv", "a"))
    for key, val in GraphData.items():
        w.writerow([key, val])