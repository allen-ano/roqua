"""
测试用
"""
import json, re


def extract_ne(line):
    line = line.lower()
    pattern = "entities: (.+)\n"
    res = re.search(pattern, line)
    if res is None:
        # print("None:"+line)
        return None
    res = res[1]
    r = re.split('[ ,，、]', res)
    r = list(filter(None, r))
    return r

fname = "data/yelp_enriched_review.json"
with open(fname) as f:
    lines = f.readlines()

num = {}
k = 0
for line in lines:
    line = line.lower()
    dic = json.loads(line)
    review = dic['review']
    entities = extract_ne(review)
    # print(entities)
    if entities is None: continue

    for item in entities:
        if item in num:
            num[item] = num[item]+1
        else:
            num[item] = 1

    # if k>2: break
    # k += 1

import operator
sorted_num = sorted(num.items(), key=operator.itemgetter(1), reverse=True)

fname = "data/entities.txt"
fin = open(fname, "wt")

for key, value in sorted_num:
    fin.write(f"{key}:{value}\n")
fin.close()