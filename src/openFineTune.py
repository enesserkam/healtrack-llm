import os
import gc
import torch

import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
from transformers import Trainer
from peft import LoraConfig
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


class ModelTrainer:
    def __init__(self, model_name, new_model, tokenizer, dataset):
        self.model_name = model_name
        self.new_model = new_model
        self.tokenizer = tokenizer
        self.dataset = dataset
        self.model = self.load_model()
        self.training_args = self.set_training_arguments()
        self.trainer = self.create_trainer()

    def load_model(self):
        # Load model with CPU-compatible settings
        model = AutoModelForCausalLM.from_pretrained(self.model_name)
        model.config.use_cache = False
        return model

    def set_training_arguments(self):
        # Configure training arguments
        return TrainingArguments(
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            gradient_checkpointing=True,
            learning_rate=5e-5,
            lr_scheduler_type="cosine",
            max_steps=200,
            save_strategy="no",
            logging_steps=1,
            output_dir=self.new_model,
            optim="adamw_torch",
            warmup_steps=100,
            report_to="wandb",
        )

    def create_trainer(self):
        # Create a trainer with the given model, arguments, and training dataset
        return Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.dataset,
            tokenizer=self.tokenizer
        )

    def train_model(self):
        self.trainer.train()


def main():
    formData = FormatData()
    formData.saveColumns()
    formData.createTokenizer()
    formData.formatDataset()

    print("Sample data:", formData.finalDataset[0])
    print("-----------------TOTAL SAMPLES----------------------\n")
    print("Total samples:", len(formData.finalDataset))

    model_trainer = ModelTrainer(model_name, new_model, formData.tokenizer, formData.finalDataset)
    model_trainer.train_model()


if __name__ == '__main__':
    main()
