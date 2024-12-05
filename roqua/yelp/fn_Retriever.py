"""
Retriever includes two modules: searching and ranking
BegRetriever uses beg-reranker-large of BAAI as cross encoder
"""
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import qparser
import numpy as np
from whoosh.query import Term, And

from yelp.fn_Encoder import TxtEncoder
from sklearn.metrics.pairwise import cosine_similarity
from yelp.fn_VectorDB import VectorDB
from yelp.fn_QueryRewriter import ReWriter
from llm import Qwen
from yelp.parameters import Parameters as param
import torch, re
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torch import nn

class BegRetriever:
    def __init__(self, sim_th=0.2):
        self.tokenizer = AutoTokenizer.from_pretrained('/root/autodl-tmp/beg-reranker')
        self.encoder = AutoModelForSequenceClassification.from_pretrained('/root/autodl-tmp/beg-reranker')
        self.ix = open_dir(param.indexdir)
        self.sim_th = sim_th

    # 因为QueryParser解析查询产生的term,太多。故不用QueryPaser, 自己创建query对象。与关心的查询对象
    def create_query(self, field, terms):
        tlist = []
        for term in terms:
            tlist.append(Term(f"{field}", f"{term}"))
        return And(tlist)

    def run(self, q_target, q_topic, is_query):
        ids, topics = self.search(q_target, is_query)
        # print(f"Searched reviews: {len(ids)}")

        if len(ids) == 0:
            print("Fail to search related reviews!")
            return None
        elif len(ids) <= 10:
            return ids
        else:
            index = self.rank(q_topic, ids, topics)
            # print(f"Rank choice: {len(index)}")
            return index

    def search(self, target, is_query):
        # 从倒排索引中进行检索，返回评论编号集合。is_query为True即把question作为query,
        # 否则是把抽取的target作为term进行检索
        searcher = self.ix.searcher()
        if is_query:
            query = QueryParser("content", self.ix.schema, group=qparser.OrGroup).parse(target)
        else:
            r = re.split('[, .]', target)
            tlist = list(filter(None, r))
            query = self.create_query("content", tlist)

        # print(query)
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

        if len(sim_idx) > 200:          # 挑选前200个
            sim_idx = sim_idx[:200]

        index = ids[sim_idx]

        return index

def test1():   # Beg
    query = "How about steaks in this restaurant?"

    llm = Qwen()
    model = ReWriter(llm)
    target, topic, _ = model.get(query)
    # search_targets = ' '.join(target)
    # topic = topic[0]
    search_targets = target
    print(search_targets)
    print(topic)

    retriever = BegRetriever()
    index = retriever.run(search_targets, topic, is_query=False)
    print(index)

if __name__ == '__main__':
    test1()


