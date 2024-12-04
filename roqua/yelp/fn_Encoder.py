"""
文本编码器
"""
from transformers import AutoModel, AutoTokenizer
import numpy as np


class TxtEncoder():
    def __init__(self, checkpoint): # 评论数据库和向量数据库
        device = "cuda"
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
