"""
Vector DB with Milvus
"""
import numpy as np
from pymilvus import MilvusClient

class VectorDB:
    def __init__(self, vdb, dim, newdb=False):   # newdb, 创建新的数据库，否则读入已有数据库
        self.client = MilvusClient(vdb)
        self.dim = dim

        # 创建collection
        if newdb:
            self.client.drop_collection(collection_name="my_collection")
            self.client.create_collection(
                collection_name="my_collection",
                dimension=self.dim
                )

    def size(self):
        res = self.client.query(
            collection_name="my_collection",
            output_fields=["count(*)"]
        )
        return res[0]["count(*)"]

    # 将数据添加到数据库中
    def insert(self, data):
         res = self.client.insert(collection_name="my_collection", data=data)

    # 根据id检索embeddings，返回numpy的数组结构
    def get(self, ids, limit=1000): # query应该是个列表
        res = self.client.get("my_collection", ids=ids)
        embeds = np.zeros((len(res), self.dim))
        ids = []

        for id, item in enumerate(res):
            vec = item['vector']
            ids.append(item['id'])
            embeds[id] = vec

        return embeds, ids
