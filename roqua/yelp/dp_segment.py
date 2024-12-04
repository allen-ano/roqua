"""
segment long reviews to the list of short sentences.
"""

from yelp.parameters import Parameters as params
import sqlite3
from yelp.llm_prompts import SEGMENT_REVIEW, EXTRACT_NE_PROMPT
import re
from llm import Qwen

srid = 0

# 1. reading reviews and load LLM
def load():
    con = sqlite3.connect(params.rdb)
    cur = con.cursor()
    sql = "SELECT id, contents FROM reviews"
    res = cur.execute(sql)
    res = res.fetchall()
    cur.close()
    con.close()
    llm = Qwen()
    return res, llm

def insert(rid,response, cur, llm):
    global srid

    p1 = "[0-9]+\.(.+)\:"
    response = response.strip().lower()
    rlist = response.split('\n')

    for line in rlist:
        line = line.strip()
        res = re.search(p1, line)
        if res is None: continue

        topic = res[1].strip()
        if topic == "none": continue

        idx = line.find(':')
        review = line[idx+1:].strip()
        entity = extract_entity(llm, review)
        if entity == "none": continue

        review = str.replace(review, "\"","'")
        topic = str.replace(topic, "\"", "'")
        entity = str.replace(entity, "\"","'")

        sql = f"""INSERT INTO reviews VALUES ({srid}, {rid}, "{review}","{topic}","{entity}")"""
        srid += 1
        # print(sql)
        try:
            cur.execute(sql)
        except:
            print(sql)
    return

def segment(llm, rid, review, cur):
    sys_content = """You are an expert on text analysis."""
    usr_content = SEGMENT_REVIEW.format(review)
    messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}, ]

    res = llm.call_with_message(messages)
    insert(rid, res, cur, llm)
    return

def extract_entity(llm, review):
    sys_content = """You are an expert on text analysis."""
    usr_content = EXTRACT_NE_PROMPT.format(review)
    messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}, ]

    entities = llm.call_with_message(messages)
    entities = entities.lower()

    if "entities:" in entities:
        idx = entities.find("entities:")+8
        res = entities[idx+1:].strip()
    else:
        res = "none"
    return res

# 2. segment
def run(res, llm):
    con = sqlite3.connect(params.rdb_short)
    cur = con.cursor()

    k = 0
    for item in res:
        rid = item[0]
        review = item[1]
        segment(llm, rid, review, cur)
        con.commit()

        # if k > 10 : break
        k += 1
        if k%10 == 0 : print(k, end=" ")

    cur.close()
    con.close()

if __name__ == '__main__':
    # line = "the food is very good, the prices fair and the atmosphere can't be beat!"
    # res = extract(line)
    # print(res)
    res, llm = load()
    run(res, llm)