"""
检索器，包括search和rank两个模块
有两个类，在ranking模块使用的模型不同：
一个是使用bert-chinese, 预先产生了每条评论的topic的表示向量，存储在了向量数据库
另一个是使用BAAI的beg-reranker-large模型作为cross encoder。查询和评论的topic都以文本的形式送入模型
"""
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import qparser
import numpy as np
from whoosh.query import Term, And, Or

from douyin.fn_Encoder import BertTxtEncoder
from sklearn.metrics.pairwise import cosine_similarity
from douyin.fn_VectorDB import VectorDB
from douyin.fn_QueryRewriter import ReWriter
from douyin.llm import Qwen
from douyin.parameters import Parameters as param

class BertRetriever:
    def __init__(self, encoder, tdb, th=0.9):  # th是选择评论的阈值
        self.ix = open_dir("data/indexdir")
        device = "cuda"
        self.encoder = encoder
        self.tdb = tdb              # topic vector db
        self.sim_th = th

    def search(self, target):  # 从倒排索引中进行检索，返回评论编号集合
        searcher = self.ix.searcher()
        # query = QueryParser("content", ix.schema).parse(sentence)
        query = QueryParser("content", self.ix.schema, group=qparser.OrGroup).parse(target)
        results = searcher.search(query, limit=None)
        # reviews = []
        ids = []
        for item in results:
            # reviews.append(item['content'])
            ids.append(item['id'])

        return ids

    # 根据检索到的评论编号集合，用评论的topic和查询计算余弦相似度进行ranking
    def rank(self,query, ids):  # ids: 检索到的评论编号集合
        query_vec = self.encoder.get_embed(query)
        embeds, ids = self.tdb.get(ids)
        sim = cosine_similarity(query_vec, embeds)[0]
        sim_idx = np.argsort(sim)[::-1]
        print(sim[sim_idx])

        ids = np.array(ids)
        index = ids[sim_idx]

        return index


import torch, re
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torch import nn

class BegRetriever:
    def __init__(self, sim_th=0.1):
        self.tokenizer = AutoTokenizer.from_pretrained('/root/autodl-tmp/beg-reranker')
        self.encoder = AutoModelForSequenceClassification.from_pretrained('/root/autodl-tmp/beg-reranker')
        self.ix = open_dir(param.indexdir)
        self.sim_th = sim_th
        self.rank_choose = 200

    # 因为QueryParser解析查询产生的term,太多。故不用QueryPaser, 自己创建query对象。与关心的查询对象
    def create_AND_query(self, field, terms):
        tlist = []
        for term in terms:
            tlist.append(Term(f"{field}", f"{term}"))
        return And(tlist)

    def create_OR_query(self, field, terms):
        tlist = []
        for term in terms:
            tlist.append(Term(f"{field}", f"{term}"))
        return Or(tlist)

    def run(self, q_target, q_topic, is_and=True, sim_th=0.1, rank_choose=200):
        self.sim_th = sim_th
        self.rank_choose=rank_choose
        ids, topics = self.search(q_target, is_and)
        print(f"Searched reviews: {len(ids)}")

        if len(ids) < 2:
            print("未搜索到相关评论！")
            return None

        index = self.rank(q_topic, ids, topics)
        print(f"Rank choice: {len(index)}")
        return index

    # 实验：只使用BM25
    def run2(self, query):
        searcher = self.ix.searcher()
        query = QueryParser("content", self.ix.schema, group=qparser.OrGroup).parse(query)
        results = searcher.search(query, limit=20)

        ids = []
        for item in results:
            ids.append(item['id'])

        return ids

    def search(self, target, is_and):
        # 从倒排索引中进行检索，返回评论编号集合。is_query为True即把question作为query,
        # 否则是把抽取的target作为term进行检索
        searcher = self.ix.searcher()
        if is_and:
            query = self.create_AND_query("content", target)
        else:
            query = self.create_OR_query("content", target)

        print(query)

        results = searcher.search(query, limit=200)

        topics = []
        ids = []
        for item in results:
            topics.append(item['topic'])
            ids.append(item['id'])

        return ids, topics

    def rank(self,query, ids, topics):  # ids: 检索到的评论编号集合
        pairs = []
        for topic in topics:
            pairs.append([query, topic])
        m = nn.Sigmoid()
        with torch.no_grad():
            inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
            scores = self.encoder(**inputs, return_dict=True).logits.view(-1, ).float()
            sim = m(scores).detach().cpu().numpy()

        ids = np.array(ids)
        sim_idx = sim > self.sim_th
        sim = sim[sim_idx]
        ids = ids[sim_idx]
        sim_idx = np.argsort(sim)[::-1]

        if len(sim_idx) > self.rank_choose:          # 挑选前rank_choose个
            sim_idx = sim_idx[:self.rank_choose]

        index = ids[sim_idx]

        return index

def test1():   # Beg
    query = "北京的天气如何？"

    llm = Qwen()
    model = ReWriter(llm)
    target, topic, _ = model.get(query)
    search_targets = ' '.join(target)
    topic = topic[0]
    print(search_targets)
    print(topic)

    retriever = BegRetriever()
    index = retriever.run(search_targets, topic, is_query=False)
    print(index)

def test2():  # bert
    dbname = param.topic_vdb
    tdb = VectorDB(dbname, 768, False) # topic vector db
    encoder = BertTxtEncoder()
    query = "北京的节日旅游如何？"
    model = ReWriter()
    target, topic, _ = model.get(query)
    search_targets = ' '.join(target)
    topic = topic[0]
    print(search_targets)
    print(topic)

    retriever = BertRetriever(encoder, tdb)
    ids = retriever.search(search_targets)
    # print(ids)
    index = retriever.rank(topic, ids)
    # print(index)


if __name__ == '__main__':
    test1()


