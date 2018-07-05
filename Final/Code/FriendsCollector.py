import tweepy
import sys
import operator
import networkx as nx
from time import sleep
import matplotlib.pyplot as plt
from os import listdir
from getHistogram import *
from graphAnalyzer import *

colorlist = [ 'r', 'g', 'b', 'c', 'm', 'y', 'k' ]


class Twitter:
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = {
                "consumer_key": "sjSMNhB8w5AFjZUFNGZOt61Pw",
                "consumer_secret": "3HJ3bZao1VqRGCDtKWdqZKm56u0wOJpAe3LFPTnsLKeLzOdBNu",
                "access_token": "92355149-EZlaulb6Iz5vfoMMVLwghMA2fhO85HOLmUpVmrFN9",
                "access_token_secret": "4239COvibkVjp0L7RYjIZVNV5gIRCIcONdEHiIlRDEKVV"
            }
        else:
            cfg = {
                "consumer_key": cfg["consumer_key"],
                "consumer_secret": cfg["consumer_secret"],
                "access_token": cfg["access_token"],
                "access_token_secret": cfg["access_token_secret"]
            }

        auth = tweepy.OAuthHandler(cfg["consumer_key"], cfg["consumer_secret"])
        auth.set_access_token(cfg["access_token"], cfg["access_token_secret"])
        self.api = tweepy.API(auth)

    #Get a the followers of the current user
    def get_followers(self, user_id=None):
        if user_id is None:
            return tweepy.Cursor(self.api.followers_ids).items()
        else:
            return tweepy.Cursor(self.api.followers_ids, id=user_id).items()
    #Build Graph. Collect all followers, followers of followers
    # followers of followers of followers etc..
    def build_graph(self, origin_user_id=None):
        graph = nx.DiGraph()
        graph.add_node(origin_user_id,id=origin_user_id)
        visited = [origin_user_id]
        j=0
        for now_id in visited:
            followers = self.get_followers(now_id)
            i = 0
            while True:
                try:
                    follower_id = followers.next()
                    i+=1
                    if follower_id not in visited:
                        visited.append(follower_id)
                    if follower_id not in graph.neighbors(now_id):
                        graph.add_node(follower_id)
                        graph.add_edge(now_id,follower_id)
                    # test with a small graph, limiting just to 20 friends each node
                    if i >= 20:
                        break
                #Hit limit
                except tweepy.TweepError:
                    showHisto(graph)
                    Analyze(graph)
                    log_cetrality(graph)
                    print("Rate limited. Sleeping for 15 minutes.")
                    sleep(15 * (60))
                    continue
                    break
                except StopIteration:
                    break
            self.draw_graph(graph,j)
            if(j==len(colorlist)): 
                j=0
            else: j+=1
        return graph

    def draw_graph(self, graph,index):
        plt.clf()
        pos = nx.spring_layout(graph, iterations=200)
        nx.draw(graph,pos,node_color='b', node_size=85, cmap=plt.cm.Blues)
        #nx.draw_networkx_nodes(graph, pos, node_size=85, node_color=colorlist[index],edge_color=colorlist[index])
        #nx.draw_networkx_edges(graph, pos)
        plt.title("Friends Graph")
        plt.draw()
        plt.pause(0.5)
        plt.savefig("finalGraph")

def log_cetrality(graph):
    if(len(graph)==1):
        print("Empty Graph")
        return None
    GraphCen=nx.eigenvector_centrality(graph)
    w = csv.writer(open("./output/centr.csv", "a"))
    for key, val in GraphCen.items():
        w.writerow([key, val])
    print("User with highset centrality:"+str(max(GraphCen.iteritems(),key=operator.itemgetter(1))[0]))
    return None

def main():
    user_name = "realDonaldTrump"
    twitter = Twitter()
    user_id = twitter.api.get_user(user_name).id
    twitter.build_graph(user_id)



if __name__ == "__main__":
    main()
