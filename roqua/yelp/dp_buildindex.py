"""
build inverted index for search engine
"""
import json

from whoosh.index import create_in, open_dir
from whoosh.fields import TEXT, Schema, NUMERIC, STORED
from jieba.analyse import ChineseAnalyzer
import sqlite3
from whoosh.qparser import QueryParser
from whoosh import qparser
import re
from yelp.parameters import Parameters as params

#从enriched reviews 建立搜索引擎
def extract_topic(line):
    pattern = "topics: (.+)\n"
    res = re.search(pattern, line)
    if res is None:
        return None
    res = res[1]
    return res

def build_index(indexdir, enriched_review):
    k = 0
    schema = Schema(id=NUMERIC(stored=True), topic=STORED(), content=TEXT(stored=True))
    ix = create_in(indexdir, schema)
    writer = ix.writer()

    with open(enriched_review) as f:
        lines = f.readlines()

    for line in lines:
        line = line.lower()
        dic = json.loads(line)
        id = dic['id']
        review = dic['review']
        topic = extract_topic(review)
        if topic is None: continue

        writer.add_document(id=id, topic=topic, content=review)
        # if k>10: break
        k += 1

    writer.commit()

def search(sentence): # for testing
    ix = open_dir(params.indexdir)
    searcher = ix.searcher()
    # query = QueryParser("content", ix.schema).parse(sentence)
    query = QueryParser("content", ix.schema, group=qparser.OrGroup).parse(sentence)
    results = searcher.search(query,limit=None)
    results = results.copy()
    for i in range(5):
        print(results[i]['topic'])
        print(results[i]['content'])
    searcher.close()

    print(results)

    # for item in results:
    #     print(item['content'])
if __name__ == '__main__':
    line = "have a high quality foods"
    search(line)