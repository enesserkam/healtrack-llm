from llama_cpp import Llama

def main():
    # Initialize the Llama model
    llm = Llama(
        model_path="./capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
        n_ctx=32768,
        n_threads=12,
        n_gpu_layers=0  # Set to 0 if no GPU is available
    )

    # Chat loop
    print("You can start chatting with the model (type 'quit' to exit).")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        # Generate a response
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are a health advise assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        print("AI:", response)


if __name__ == "__main__":
    main()
