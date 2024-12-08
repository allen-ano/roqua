"""
extracting entities and topics
"""
from llm import Qwen
from yelp.llm_prompts import GET_NE_TOPIC_PROMPT
import re

class ReWriter:
    def __init__(self, llm):
        self.model = llm

    def get(self, query):
        sys_content = """You are an expert on natural language processing."""
        usr_content = GET_NE_TOPIC_PROMPT.format(query)
        messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}, ]
        res = self.model.call_with_message(messages)
        target = self.extract_ne(res)
        topic = self.extract_topic(res)
        return target, topic, res

    def extract_topic(self, line):
        line = line.lower()
        pattern = "topics: (.+)"
        res = re.search(pattern, line)
        if res is None:
            # print("None:"+line)
            return None
        res = res[1]
        # r = re.split('[ ,，、]', res)
        # r = list(filter(None, r))
        return res

    def extract_ne(self, line):
        line = line.lower()
        pattern = "entities: (.+)\n"
        res = re.search(pattern, line)
        if res is None:
            # print("None:"+line)
            return None
        res = res[1]
        # r = re.split('[ ,，、]', res)
        # r = list(filter(None, r))
        return res

if __name__ == '__main__':
    query = "how about steaks?"
    llm = Qwen()
    model = ReWriter(llm)
    target, topic, _ = model.get(query)
    print(target)
    print(topic)
