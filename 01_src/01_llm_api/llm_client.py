from openai import OpenAI
import os

def create_client(base_url):
    return OpenAI(
        base_url=base_url,
        api_key="dummy"
    )

def ask_llm(client, model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("Select LLM Backend:")
    print("1 → vLLM")
    print("2 → Ollama")

    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        base_url = "http://192.168.37.145:8000/v1"
        model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        print("Using vLLM...")
    elif choice == "2":
        base_url = "http://localhost:11434/v1"
        model = "phi3"   # example Ollama model
        print("Using Ollama...")
    else:
        print("Invalid choice")
        exit()

    client = create_client(base_url)

    prompt = input("Enter your question: ")

    answer = ask_llm(client, model, prompt)

    print("\nResponse:\n")
    print(answer)