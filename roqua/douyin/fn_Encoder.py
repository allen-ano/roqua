"""
文本编码器
"""
from transformers import AutoModel, AutoTokenizer
import numpy as np
from douyin.parameters import Parameters as param

# 文本编码器父类
class TxtEncoder:
    def get_embed(self, reviews):
        raise NotImplementedError

# 基于chinese bert创建的一个文本编码器子类
class BertTxtEncoder(TxtEncoder):
    def __init__(self): # 评论数据库和向量数据库
        device = "cuda"
        checkpoint = param.encoder
        self.model = AutoModel.from_pretrained(checkpoint).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    def get_embed(self, reviews):
        inputs = self.tokenizer(reviews, padding=True, truncation=True, return_tensors="pt")['input_ids'].to("cuda")
        outputs = self.model(inputs).last_hidden_state
        # outputs2 = torch.mean(outputs, dim=1)
        # query_vec = outputs2.detach().cpu()
        query_vec = outputs[:, 0, :].detach().cpu()
        vec = np.array(query_vec)

        # return query_vec.float().numpy()
        return vec


# to do： 实施其他模型的编码器

