import tweepy
import sys
import operator
import networkx as nx
from time import sleep
import matplotlib.pyplot as plt
from os import listdir
from getHistogram import *
from graphAnalyzer import *



class Twitter:
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = {
                "consumer_key": "AuoBYVpE0h7uBJLVr422x6CRU",
                "consumer_secret": "RuFZ79MxQKzs5WFBmLrtMseaFGGPLLLyd9sPkE6H9zjQl20mGV",
                "access_token": "92355149-AByhC72BR043wZgLiFBo0mjjhVcH7fbgjHrV9BzEl",
                "access_token_secret": "5GRFjZQdpokLDY8003YkM228BQXmDynwAzlV3BTqQgs6P"
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
        graph = nx.Graph()
        graph.add_node(origin_user_id,id=origin_user_id)
        visited = [origin_user_id]
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
                    # test with a small graph, limiting just to 10 friends each node
                    if i >= 10:
                        break
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
            nx.coloring.greedy_color(graph, strategy=nx.coloring.strategy_largest_first)
            self.draw_graph(graph)
        return graph

    def draw_graph(self, graph):
        plt.clf()
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=85, node_color='b')
        nx.draw_networkx_edges(graph, pos)
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
    user_name = "ladygaga"
    twitter = Twitter()
    user_id = twitter.api.get_user(user_name).id
    twitter.build_graph(user_id)



if __name__ == "__main__":
    main()
