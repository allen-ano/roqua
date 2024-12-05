"""
使用通义千问大模型进行观点挖掘
"""

import json, re
import numpy as np
from douyin.llm_prompts import ENRICH_REVIEW_PROMPT, QUESTION_REVIEW_RELATIVE,OPINION_SUMMARIZE_PE, OPINION_SUMMARIZE_COT


class OpinionMiner:
    def __init__(self, llm):
        self.model = llm

    # 挑选与问题相关的评论
    def choose_related_reviews(self, question, reviews):
        sys_content = """你是一个文本分析的专家。"""
        s = ""
        for id, r in enumerate(reviews):
            s += f"{id}. '{r}'\n"
        usr_content = QUESTION_REVIEW_RELATIVE.format(question, s)
        messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}]
        res = self.model.call_with_message(messages)
        return res

    # 从相关性判断结果里抽取出，相关性评论的下标列表
    def extract_index(self, response):
        pattern = "([0-9]+)"
        response = str.lower(response)
        rlist = response.split('\n')

        idx = []
        for item in rlist:
            if 'yes' in item:
                res = re.search(pattern, item)
                idx.append(int(res[0]))

        return idx

    def summarize_opinion(self, question, reviews, num=30):
        # print(reviews)
        response = self.choose_related_reviews(question, reviews)
        idx = self.extract_index(response)
        if len(idx) == 0: return "没有相关信息！"

        reviews = np.array(reviews)[idx]
        s = ""
        for item in reviews:
            s += item+"\n"

        # print(s)
        sys_content = """你是一个文本分析的专家。"""
        usr_content = OPINION_SUMMARIZE_PE.format(question, s, num)   # LLM有更大的总结能力
        # usr_content = OPINION_SUMMARIZE_COT.format(question, s, num)   # 限制了LLM幻觉

        messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}]
        res = self.model.call_with_message(messages)
        return res

    def summrize_opinion_again(self, question, response):
        sys_content = """你是一个文本分析的专家。"""
        usr_content = f"""
        标记Question中保存的是用户提出的问题。
        标记Response中保存的是上一次针对用户问题产生的答案。
        ###
        Question:
        {question}
        ###
        Response:
        {response}
        ###
        请根据用户提交的问题对上一次产生的答案再一次进行总结。使得答案更简介。步骤如下：
        1. 如果所有的内容都是"没有相关信息"，则停止总结，返回文本"没有相关信息"。
        2. 仅仅根据给定的内容进行总结，产生答案。
        字数限制在30字以内。
        """
        messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}]

        res = self.model.call_with_message(messages)
        return res

    # 从一条评论中抽取实体，话题和分析过程
    def enrich_review(self, review):
        sys_content = """
        你是一个自然语言处理领域的专家。
        """
        usr_content = ENRICH_REVIEW_PROMPT.format(review)
        res = self.model.call_with_message(sys_content, usr_content)
        return res




