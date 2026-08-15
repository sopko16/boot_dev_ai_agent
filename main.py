import os
from dotenv import load_dotenv
import argparse
from prompts import system_prompt

def call_llm(prompt:str="", verbose:bool=False):
    from openai import OpenAI

    api_key = os.environ.get("O_R_K")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages,

    )

    if verbose:
        print(f"User prompt: {prompt}")
        print("Model used:", response.model)
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print("Response:")
    print(response.choices[0].message.content)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    prompt = args.user_prompt
    call_llm(prompt,args.verbose)




if __name__ == "__main__":
    main()
