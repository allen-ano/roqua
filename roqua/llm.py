"""
A class for using Qwen LLM
"""

from transformers import AutoModelForCausalLM, AutoTokenizer,AutoModel

class Qwen:
    def __init__(self):
        device = "cuda"
        checkpoint = '/root/autodl-tmp/qwen2-7b'  # path to LLM

        self.model = AutoModelForCausalLM.from_pretrained(
            checkpoint,
            torch_dtype="auto",
            device_map="auto"
        ).to(device)

        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    def call_with_message(self, messages):
        # messages = [{'role': 'system', 'content': sys_content}, {'role': 'user', 'content': usr_content}, ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to("cuda")

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

    # for multi-runs conversation. The returned message contains information in current run.
    def multiruns(self, messages):
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to("cuda")

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        messages.append({'role': 'assistant', 'content': response})
        return response, messages

if __name__ == '__main__':
    llm = Qwen()