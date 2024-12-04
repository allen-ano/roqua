"""
generate enriched reviews
"""
from yelp.llm_prompts import ENRICH_REVIEW_PROMPT
import numpy as np
import sqlite3
import pandas as pd
import json
from llm import Qwen

def enrich_review(review, model):
    sys_content = """
       You are an expert in natural language processing (NLP).
       """
    usr_content = ENRICH_REVIEW_PROMPT.format(review)
    messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}, ]
    res = model.call_with_message(messages)
    return extract(res)

def extract(txt):
    lines = txt.split("\n")
    s = ""
    for line in lines:
        line = line.lower()
        if "entities:" in line:
            s += line + "\n"
        if "topics:" in line:
            s += line + "\n"
        if "analysis:" in line:
            s += line + "\n"

    return s

def run(rdb, enriched_reviews):    
    model = Qwen()
    con = sqlite3.connect(rdb)
    cur = con.cursor()
    sql = "SELECT id, contents FROM reviews"

    res = cur.execute(sql)
    res = res.fetchall()

    cur.close()
    con.close()

    er_json = open(enriched_reviews, 'w', encoding="utf8")
    k = 0
    for item in res:
        id = item[0]
        review = item[1]
        res = enrich_review(review, model)

        # print(id)
        # print(res)
        res = review + "\n" + res
        record = {}
        record['id'] = id
        record["review"]=res
        json.dump(record, er_json, ensure_ascii=False)
        er_json.write("\n")
        k += 1
        # if k>10: break
        if k % 100 ==0 : print(f"{k} ")

    er_json.close()

