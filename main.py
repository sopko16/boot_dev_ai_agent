import os
from dotenv import load_dotenv

def call_llm(prompt:str=""):
    from openai import OpenAI

    api_key = os.environ.get("O_R_K")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages,

    )

    print(f"User prompt: {prompt}")
    print("Model used:", response.model)
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")
    print(response.choices[0].message.content)


def main():
    load_dotenv()

    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    call_llm(prompt)




if __name__ == "__main__":
    main()
