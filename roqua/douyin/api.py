"""
Main interface for using ROQuA on Douyin
"""
from douyin.fn_QueryRewriter import ReWriter
from douyin.fn_Retriever import BegRetriever
from douyin.fn_TxtClustering import Clustering
from douyin.fn_OpinionMiner import OpinionMiner
from douyin.parameters import Parameters as param
import jieba

class DouyinAPI:
    def __init__(self, llm):
        self.rdb = param.rdb  # reviews db
        self.rewriter = ReWriter(llm)
        self.retriever = BegRetriever()
        self.clustering = Clustering()
        self.om = OpinionMiner(llm)

    # start from here
    def run(self, query):
        # 1. Query rewriting
        target, topic, _ = self.rewriter.get(query)
        if target is None or target == "None" or target[0] == 'None':
            if topic is None or topic == "None" or topic[0] == 'None':
                return "没有相关信息"
            else:
                target = jieba.cut(topic[0], cut_all=False)   # 对于一些提取不出entity的question,
                target = list(target)
               
        search_targets = target
        topic = topic[0]
        print(search_targets)
        print(topic)

        # 2. retriever
        index = self.retriever.run(search_targets, topic)  # AND检索
        if index is None or len(index) < 2:     # 如果没有检索到相关评论
            if len(search_targets) < 2:         # 如果只有一个实体，分词后进行与检索
                temp = jieba.cut(search_targets[0], cut_all=False)  # 对于一些提取不出entity的question,
                temp = list(temp)
                if len(temp) == 1: return "没有相关信息"
                index = self.retriever.run(temp, topic)  # AND检索
                if index is None or len(index) < 2:
                    return "没有相关信息"
            else:                           # 有多个实体则进行或检索
                print("没有相关信息！进行OR检索")
                index = self.retriever.run(search_targets, topic, False, sim_th=0.2, rank_choose=40)
                if index is None or len(index) < 2:
                    return "没有相关信息"

        # 3. Clustering and opinoin mining
        if len(index) > 50:  # clustering
            print("Clustering...")
            # print(index)
            if len(index) < 70:
                clusters = self.clustering.run(self.rdb, index, k=2)
            else:
                clusters = self.clustering.run(self.rdb, index)

            response = ""
            for index, cluster in enumerate(clusters):
                if len(cluster) < 2:
                    print("没有相关信息！")
                    continue
                # print(cluster)
                opinion = self.om.summarize_opinion(query, cluster)
                response += f"{index}: {opinion}\n"
                # print(f"{index}: {opinion}")

            opinion =  response + "\n===进一步总结===\n" +self.om.summrize_opinion_again(query, response)
        else:               # 评论数量少则不聚类操作
            reviews = self.clustering.get_reviews(self.rdb, index)
            if len(reviews) == 0:
                opinion = "没有相关信息！"
            else:
                # print(reviews)
                opinion = self.om.summarize_opinion(query, reviews, num=30)

        return opinion

