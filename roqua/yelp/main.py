"""
main interface for QA model
"""

from yelp.fn_QueryRewriter import ReWriter
from yelp.fn_Retriever import BegRetriever
from yelp.fn_TxtClustering import Clustering
from yelp.fn_OpinionMiner import OpinionMiner
from llm import Qwen
from yelp.parameters import Parameters

rdb = Parameters.rdb

llm = Qwen()
rewriter = ReWriter(llm)
retriever = BegRetriever()
clustering = Clustering()
om = OpinionMiner(llm)
print("Loaded!")

# 运行
def run(query, target=None, topic=None):
    if target is None or topic is None:
        target, topic, res = rewriter.get(query)
    target = target.lower()
    topic = topic.lower()

    if topic is None or topic =='none':
        print("No topic, please change your question!")
        exit()

    if target is None or target.lower() == "none":
        print("No entities, Using question as query!")
        search_targets = query
        is_query = True
    else:
        search_targets = target
        is_query = False

    print(search_targets)
    print(topic)
    # print(res)

    index = retriever.run(search_targets, topic, is_query)
    if index is None or len(index)<1:
        if is_query:
            print("No related reviews, please change your question!")
            return
        print("没有相关评论！重新按照Question检索")
        index = retriever.run(query, topic, True)
        if index is None or len(index) < 1:
            print("No related reviews, please change your question!")
            return

    if len(index) > 30:  # clustering
        print("Clustering...")
        # print(index)
        if len(index)<70:
            clusters = clustering.run(rdb, index, k=2)
        else:
            clusters = clustering.run(rdb, index)

        response = ""
        for index, cluster in enumerate(clusters):
            if len(cluster) < 1:
                print("没有相关评论！")
                continue
            print(cluster)
            opinion = om.summarize_opinion(query, cluster)
            response += opinion+"\n"
            print(f"{index}: {opinion}")

        opinion = om.summrize_opinion_again(query, response)
        print(f"\n=== 进一步总结 ===\n{opinion}")
    else:               # 评论数量少则不聚类操作
        reviews = clustering.get_reviews(rdb, index)
        if len(reviews)==0:
            print("没有相关评论！")
        else:
            print(reviews)
            opinion = om.summarize_opinion(query, reviews, num=30)
            print(f"{opinion}")

if __name__ == '__main__':
    # === 输入查询，然后运行程序 ===
    # query = "Does this restaurant provide sushi?"
    query = "Is the waiting time at this restaurant long?"
    # target = "japanese"
    # topic = "foods"
    # run(query, target ,topic)

    run(query)
