"""
Yelp API
"""

from yelp.fn_QueryRewriter import ReWriter
from yelp.fn_Retriever import BegRetriever
from yelp.fn_TxtClustering import Clustering
from yelp.fn_OpinionMiner import OpinionMiner
from yelp.parameters import Parameters

class YelpAPI:
    def __init__(self, llm):
        self.rdb = Parameters.rdb
        self.rewriter = ReWriter(llm)
        self.retriever = BegRetriever()
        self.clustering = Clustering()
        self.om = OpinionMiner(llm)

    def run(self, query, target=None, topic=None):
        if target is None or topic is None:
            target, topic, res = self.rewriter.get(query)
        target = target.lower()
        topic = topic.lower()

        if topic is None or topic =='none':
            return("No topic, please change your question!")

        if target is None or target.lower() == "none":
            print("No entities, Using question as query!")
            search_targets = query
            is_query = True
        else:
            search_targets = target
            is_query = False

        # print(search_targets)
        # print(topic)
        # print(res)

        index = self.retriever.run(search_targets, topic, is_query)
        if index is None or len(index)<1:
            if is_query:
                return ("No relevant reviews, please change your question!")

            print("No relevant reviews! use Question as query to search again!")
            index = self.retriever.run(query, topic, True)
            if index is None or len(index) < 1:
                return("No relevant reviews, please change your question!")

        if len(index) > 50:  # clustering
            # print("Clustering...")
            # print(index)
            if len(index)<70:
                clusters = self.clustering.run(self.rdb, index, k=2)
            else:
                clusters = self.clustering.run(self.rdb, index)

            response = ""
            for index, cluster in enumerate(clusters):
                if len(cluster) < 1:
                    print("No relevant reviews")
                    continue
                # print(cluster)
                opinion = self.om.summarize_opinion(query, cluster)
                response += f"{index}: {opinion}\n"
                # print(f"{index}: {opinion}")

            opinion = self.om.summrize_opinion_again(query, response)
            return(f"{response}\n=== Further Summary ===\n{opinion}")
        else:
            reviews = self.clustering.get_reviews(self.rdb, index)
            if len(reviews)==0:
                return("No relevant information!")
            else:
                # print(reviews)
                opinion = self.om.summarize_opinion(query, reviews, num=30)
                return(opinion)


