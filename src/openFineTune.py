import os
import gc
import torch

import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
from datasets import load_dataset
import wandb

hf_token = "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"
wb_token = "b65bdd290664393a92a68f21d76febee13a3b256"
wandb.login(key=wb_token)

model_name = "automerger/YamshadowExperiment28-7B"
new_model = "UltraMerge-v2-7B"


class FormatData:
    def __init__(self):
        self.dataset = load_dataset("Intel/orca_dpo_pairs")['train']
        self.original_columns = None
        self.tokenizer = None
        self.finalDataset = None

    def saveColumns(self):
        original_cols = self.dataset.column_names
        self.original_columns = original_cols

    def createTokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "left"
        self.tokenizer = tokenizer

    def chatml_format(self, example):
        # Format system
        if len(example['system']) > 0:
            message = {"role": "system", "content": example['system']}
            system = self.tokenizer.apply_chat_template([message], tokenize=False)
        else:
            system = ""

        # Format instruction
        message = {"role": "user", "content": example['question']}
        prompt = self.tokenizer.apply_chat_template([message], tokenize=False, add_generation_prompt=True)

        # Format chosen answer
        chosen = example['chosen'] + "<|im_end|>\n"

        # Format rejected answer
        rejected = example['rejected'] + "<|im_end|>\n"

        return {
            "prompt": system + prompt,
            "chosen": chosen,
            "rejected": rejected,
        }

    def formatDataset(self):
        dataset = self.dataset.map(
            self.chatml_format,
            remove_columns=self.original_columns
        )
        self.finalDataset = dataset


formData = FormatData()
formData.saveColumns()
formData.createTokenizer()
formData.formatDataset()

print(formData.finalDataset[1])
