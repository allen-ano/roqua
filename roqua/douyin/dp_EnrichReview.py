"""
给一条评论增加更多的信息
"""
from douyin.llm_prompts import ENRICH_REVIEW_PROMPT
import numpy as np
import sqlite3
import pandas as pd
import json
from douyin.parameters import Parameters as param

# 从一条评论中抽取实体，话题和分析过程
def enrich_review(self, review):
    sys_content = """
       你是一个自然语言处理领域的专家。
       """
    usr_content = ENRICH_REVIEW_PROMPT.format(review)
    res = self.model.call_with_message(sys_content, usr_content)
    return res

def test1():    # douyin数据集
    rdb = "douyin_reviews_id.db"
    con = sqlite3.connect(rdb)
    cur = con.cursor()
    sql = "SELECT id, contents FROM reviews_id"

    res = cur.execute(sql)
    res = res.fetchall()

    cur.close()
    con.close()

    er_json  = open('douyin_enriched_review.json', 'w', encoding="utf8")
    k = 0
    for item in res:
        id = item[0]
        review = item[1]
        # print(id)
        res = enrich_review(review)
        res = review + "\n" + res
        record = {}
        record['id'] = id
        record["review"]=res
        json.dump(record, er_json, ensure_ascii=False)
        er_json.write("\n")
        # k += 1
        # if k>10: break

    er_json.close()

def test2():    # JD数据集
    fname = 'jd_enriched_review.json'
    rdb = "jd-qa.db"
    con = sqlite3.connect(rdb)
    cur = con.cursor()
    sql = "SELECT id, contents FROM reviews_id"

    res = cur.execute(sql)
    res = res.fetchall()

    cur.close()
    con.close()

    er_json  = open(fname, 'w', encoding="utf8")
    k = 0
    for item in res:
        id = item[0]
        review = item[1]
        # print(id)
        res = enrich_review(review)
        res = review + "\n" + res
        record = {}
        record['id'] = id
        record["review"]=res
        json.dump(record, er_json, ensure_ascii=False)
        er_json.write("\n")
        # k += 1
        # if k>10: break

    er_json.close()

if __name__ == '__main__':
    test2()