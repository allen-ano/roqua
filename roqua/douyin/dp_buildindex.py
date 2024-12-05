"""
为文本数据建立索引，以便搜索引擎使用
"""
import json

from whoosh.index import create_in, open_dir
from whoosh.fields import TEXT, Schema, NUMERIC, STORED
from jieba.analyse import ChineseAnalyzer
import sqlite3, re
from whoosh.qparser import QueryParser
from whoosh import qparser
from douyin.parameters import Parameters as param

#从enriched reviews 建立搜索引擎
def extract_topic(line):
    pattern = "话题[:|：](.+)[\n|分| ]"
    res = re.search(pattern, line)
    if res is None:
        # print("None:"+line)
        return None
    res = res[1]
    r = re.split('[ ,，、]', res)
    r = list(filter(None, r))
    return r

def build_index_enriched():
    k = 0
    analyzer = ChineseAnalyzer()
    schema = Schema(id=NUMERIC(stored=True), topic=STORED(), content=TEXT(stored=True, analyzer=analyzer))
    ix = create_in(param.indexdir, schema)
    writer = ix.writer()

    fname = param.enriched_reviews
    with open(fname) as f:
        lines = f.readlines()

    for line in lines:
        dic = json.loads(line)
        id = dic['id']
        review = dic['review']
        topic = extract_topic(review)
        if topic is None: continue

        writer.add_document(id=id, topic=topic[0], content=review)
        # if k>10000: break
        # k += 1

    writer.commit()

def search(sentence): # 测试用，从索引中进行检索
    ix = open_dir(param.indexdir)
    searcher = ix.searcher()
    # query = QueryParser("content", ix.schema).parse(sentence)
    query = QueryParser("content", ix.schema, group=qparser.OrGroup).parse(sentence)
    results = searcher.search(query,limit=None)

    print(results[0]['topic'])
    for item in results:
        print(item['content'])

    searcher.close()

if __name__ == '__main__':
    # build_index_enriched()
    sentence = "成都"
    search(sentence)
