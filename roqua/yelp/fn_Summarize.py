"""
Using LLM to summarize opinions
"""

import json
from llm import Qwen as llm
from llm_prompts import ENRICH_REVIEW_PROMPT

class OpinionMiner:
    def __init__(self):
        self.model = llm()

    def summarize_opinion(self, reviews, num=50):
        sys_content = """你是一个文本分析的专家。"""
        usr_content = f"""
        给你多条评论数据，你需要完成一个观点总结的任务。下面给出评论数据，每行是一条评论。
        {reviews}

        请从以上的评论总结观点，字数限制在{num}字以内。
        """

        res = self.model.call_with_message(sys_content, usr_content)
        return res

    # 从一条评论中抽取实体，话题和分析过程
    def enrich_review(self, review):
        sys_content = """
        你是一个自然语义处理领域的专家。
        """
        usr_content = ENRICH_REVIEW_PROMPT.format(review)
        res = self.model.call_with_message(sys_content, usr_content)
        return res


if __name__ == '__main__':
    e = OpinionMiner()

