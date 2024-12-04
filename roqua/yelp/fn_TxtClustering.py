"""
文本集合进行谱聚类
"""
from transformers import AutoTokenizer, AutoModel
import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
from yelp.parameters import Parameters as param

class Clustering:
    def run(self, db, review_ids, k=8):
        embeds = self.get_review_embeds(review_ids)
        cluster_review_ids = self.fit(embeds, review_ids, k=k)
        clusters = []

        for ids in cluster_review_ids:  # 获得每个簇的评论
            res = self.get_reviews(db, ids)
            clusters.append(res)

        return clusters

    # 参数embeds是评论向量数据，ids是对应的每条评论的编号。
    # 返回每个簇经过挑选后的按照距离质心排序的评论编号
    def fit(self, review_embeds, review_ids, k=8, limit=10, th=0.9994):
        review_ids = np.array(review_ids)
        clustering = SpectralClustering(n_clusters=k,
                                        assign_labels='cluster_qr',
                                        random_state=0).fit(review_embeds)
        cids = np.array(clustering.labels_)
        clusters = []
        # 处理每个簇
        for i in set(cids):
            index = cids == i
            cluster = review_embeds[index]
            ids = review_ids[index] # 当前簇每个评论的编号
            size = cluster.shape[0]
            if size <= limit: continue
            centroid = np.mean(cluster, axis=0).reshape(1, -1) # 计算质心

            sim = cosine_similarity(centroid, cluster)[0]
            sim2 = sim[sim > th]
            ids2 = ids[sim > th]

            sim_idx = np.argsort(sim2)[::-1]
            index = ids2[sim_idx]                 # 挑选距离质心最近的top个评论

            clusters.append(index)
        return clusters

    # 根据评论编号，检索它们对应的评论的embeddings
    def get_review_embeds(self,ids):
        ids = list(ids)
        vdb_name = param.review_vdb
        # vdb_name = "data/yelp_topic_milvus.db"
        from pymilvus import MilvusClient
        client = MilvusClient(vdb_name)
        res = client.get("my_collection", ids=ids, output_fields=["id", "vector"])

        import numpy as np
        review_embeds = np.zeros((len(res), 768))
        review_ids = np.zeros(len(res), dtype=np.int32)  # 矩阵review_embeds的行号和评论在数据中的编号的对应关系

        for eid, item in enumerate(res):
            review_ids[eid] = item['id']
            review_embeds[eid] = item['vector']

        return review_embeds

    # 按照评论编号检索评论数据
    def get_reviews(self, rdb, cluster_review_ids):
        cluster_review_ids = tuple(cluster_review_ids)
        if len(cluster_review_ids)==1:
            cluster_review_ids = cluster_review_ids * 2
        con = sqlite3.connect(rdb)
        cur = con.cursor()
        sql_t = "SELECT id, contents FROM reviews where id in {}"
        sql = sql_t.format(cluster_review_ids)
        res = cur.execute(sql)
        res = res.fetchall()
        cur.close()
        con.close()

        id = []
        review = []
        for line in res:
            id.append(line[0])
            review.append(line[1])

        review = np.array(review)
        sorter = np.argsort(id)
        idx = sorter[np.searchsorted(id, cluster_review_ids, sorter=sorter)]

        return review[idx]

if __name__ == '__main__':
    a = [15]
    a = a *2
    print(a)