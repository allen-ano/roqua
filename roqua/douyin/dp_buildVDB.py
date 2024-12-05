"""
建立向量数据库
有两个向量数据库，一个是每篇评论中总结的topic,为了在ranking中，查询与评论的topic进行余弦相似度的计算
第二个是每篇被enriched的评论建立向量，为了在聚类时使用
"""
import json, re
from douyin.fn_VectorDB import VectorDB
from douyin.fn_Encoder import BertTxtEncoder
from douyin.parameters import Parameters as param

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
        # print(topic)
        # if i>300: break

        r_vec = encoder.get_embed([review])[0]
        t_vec = encoder.get_embed(topic)[0]
        dic = {"id": id, "vector": r_vec}
        rlist.append(dic)

        dic = {"id": id, "vector": t_vec}
        tlist.append(dic)

        if i % 5000 == 0:
            print(i, end=" ")
            rvdb.insert(rlist)
            rlist = []
            tvdb.insert(tlist)
            tlist = []
        i += 1

    rvdb.insert(rlist)
    tvdb.insert(tlist)

def test(dbname):
    vdb = VectorDB(dbname, 768)
    client = vdb.client
    res = client.query(
        collection_name="my_collection",
        output_fields=["count(*)"]
    )
    print(res[0]["count(*)"])

if __name__ == '__main__':
    print("building vector database...")
    rfile   = param.enriched_reviews
    rdbname = param.review_vdb
    tdbname = param.topic_vdb

    encoder = BertTxtEncoder()
    rvdb = VectorDB(rdbname, 768, newdb=True)
    tvdb = VectorDB(tdbname, 768, newdb=True)

    buildVDB(rvdb, tvdb, rfile, encoder)
    print("Done!")

    test(rdbname)
    test(tdbname)


