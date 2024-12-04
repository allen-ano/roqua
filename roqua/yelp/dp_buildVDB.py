"""
building two vector DB: enriched reviews and topics
"""
import json, re
from yelp.fn_VectorDB import VectorDB
from yelp.fn_Encoder import TxtEncoder
from yelp.parameters import Parameters as params

def extract_topic(line):
    pattern = "topics: (.+)\n"
    res = re.search(pattern, line)
    if res is None:
        return None
    res = res[1]
    return res

# 从enriched reviews数据集中创建向量数据库。 包含两个向量topic的和enriched review的
def buildVDB(rvdb, tvdb, file, encoder):
    with open(file) as f:
        lines = f.readlines()

    rlist = []
    tlist = []

    i = 1
    for line in lines:
        dict = json.loads(line)
        id = dict["id"]
        review = dict["review"]
        topic = extract_topic(review)
        if topic is None: continue

        r_vec = encoder.get_embed([review])[0]
        t_vec = encoder.get_embed(topic)[0]
        dic = {"id": id, "vector": r_vec}
        rlist.append(dic)

        dic = {"id": id, "vector": t_vec}
        tlist.append(dic)

        if i % 1000 == 0:
            print(i, end=" ")
            rvdb.insert(rlist)
            rlist = []
            tvdb.insert(tlist)
            tlist = []
        i += 1

    rvdb.insert(rlist)
    tvdb.insert(tlist)

def run(reviews, rname, tname):
    print("building vector database...")
    encoder = TxtEncoder(params.encoder)
    rvdb = VectorDB(rname, 768, newdb=True)
    tvdb = VectorDB(tname, 768, newdb=True)

    buildVDB(rvdb, tvdb, reviews, encoder)
    print("Done!")

def test(dbname):
    vdb = VectorDB(dbname, 768)
    client = vdb.client
    res = client.query(
        collection_name="my_collection",
        output_fields=["count(*)"]
    )
    print(res[0]["count(*)"])

if __name__ == '__main__':
    test(params.review_vdb)
    test(params.topic_vdb)


