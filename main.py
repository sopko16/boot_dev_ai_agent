import os
from dotenv import load_dotenv
import argparse
import json
from prompts import system_prompt
from call_function import available_functions

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
        # model="openrouter/free",
        # model="nvidia/nemotron-3-ultra-550b-a55b:free",
        # model="nvidia/nemotron-3-nano-30b-a3b:free",
        model="nvidia/nemotron-3.5-lightning:free",
        messages= messages,
        tools=available_functions,
    )

    if verbose:
        print(f"User prompt: {prompt}")
        print("Model used:", response.model)
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print("Response:")
    
    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print(message.content)


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
