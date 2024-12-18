"""
opinion summarization using LLM

"""

import json, re
import numpy as np
from yelp.llm_prompts import QUESTION_REVIEW_RELATIVE, OPINION_SUMMARIZE_COT, OPINION_SUMMARIZE_PE
from yelp.llm import  Qwen

class OpinionMiner:
    def __init__(self, llm):
        self.model = llm

    # choosing reviews related with question
    def choose_related_reviews(self, question, reviews):
        sys_content = """You are an expert on text analysis."""
        s = ""
        for id, r in enumerate(reviews):
            s += f"{id}. '{r}'\n"
        usr_content = QUESTION_REVIEW_RELATIVE.format(question, s)
        messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}]
        res = self.model.call_with_message(messages)
        return res

    # extracting index of related reviews
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
        response = self.choose_related_reviews(question, reviews)
        idx = self.extract_index(response)
        if len(idx) == 0: return "No relevant information!"

        reviews = np.array(reviews)[idx]
        s = ""
        for item in reviews:
            s += item+"\n"

        # print(s)
        sys_content = """You are an expert on text analysis."""
        usr_content = OPINION_SUMMARIZE_PE.format(question, s, num)
        # usr_content = OPINION_SUMMARIZE_COT.format(question, s, num)    # limit hallucination

        messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}]
        res = self.model.call_with_message(messages)
        return res

    def summrize_opinion_again(self, question, response):
        sys_content = """You are an expert on text analysis."""
        usr_content = f"""
        User's question is marked with the 'Question' tag. Reviews are listed under the 'Reviews' tag. 
        ######
        Question: {question}
        ######
        Reviews: 
        {response}
        ######
        Please summarize the reviews' opinions in 30 words or less based on the question. 
        If the reviews are irrelevant or absent, respond with "No information".
        """
        messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}]

        res = self.model.call_with_message(messages)
        return res

if __name__ == '__main__':
    llm = Qwen()
    e = OpinionMiner(llm)


