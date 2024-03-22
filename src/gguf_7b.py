from llama_cpp import Llama

llm = Llama(
  model_path="../capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",  # Download the model file first
  n_ctx=1024,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=4
)

print("input")
output = llm(
  "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant", # Prompt
  max_tokens=256,
  stop=["</s>"],
  echo=True
)
print("output")
llm = Llama(model_path="../capybarahermes-2.5-mistral-7b.Q4_K_M.gguf", chat_format="llama-2")  # Set chat_format according to the model you are using
response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a story writing assistant."},
        {
            "role": "user",
            "content": "Write a story about llamas."
        }
    ]
)
print(response)
