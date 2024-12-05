"""
查询改写，一是抽取其中的entities，二是提炼它的topic
"""
from douyin.llm_prompts import GET_TARGET_TOPIC_PROMPT, GET_NE_TOPIC_PROMPT
import re

class ReWriter:
    def __init__(self, llm):
        self.model = llm

    def get(self, query):
        sys_content = """你是一个自然语言处理领域的专家。"""
        usr_content = GET_NE_TOPIC_PROMPT.format(query)
        messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}, ]
        res = self.model.call_with_message(messages)
        target = self.extract_ne(res)
        topic = self.extract_topic(res)
        return target, topic, res

    def extract_topic(self, line):
        pattern = "话题[:|：](.+)"
        res = re.search(pattern, line)
        if res is None:
            # print("None:"+line)
            return None
        res = res[1]
        r = re.split('[ ,，、]', res)
        r = list(filter(None, r))
        return r

    def extract_ne(self, line):
        pattern = "实体[:|：](.+)[\n| ]"
        res = re.search(pattern, line)
        if res is None:
            # print("None:"+line)
            return None
        res = res[1]
        r = re.split('[ ,，、]', res)
        r = list(filter(None, r))
        return r
