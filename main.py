import os
from dotenv import load_dotenv
import argparse
import json
from prompts import system_prompt
from call_function import available_functions, call_function

# TODO: MOVE THIS TO A CLASS:
def create_llm_client():
    from openai import OpenAI

    api_key = os.environ.get("O_R_K")

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def call_llm_once(client, messages, verbose:bool=False):

    response = client.chat.completions.create(
        # model="openrouter/free",
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        # model="nvidia/nemotron-3-nano-30b-a3b:free",
        # model="nvidia/nemotron-3.5-lightning:free",
        messages= messages,
        tools=available_functions,
    )

    if verbose:
        # print(f"User prompt: {prompt}")
        print("Model used:", response.model)
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print("Response:")

    return response.choices[0].message    
    # message = response.choices[0].message
    # if message.tool_calls:
    #     for tool_call in message.tool_calls:
    #         # function_args = json.loads(tool_call.function.arguments or "{}")
    #         # print(f"Calling function: {tool_call.function.name}({function_args})")
    #         result_message = call_function(tool_call)

    #         if not result_message["content"]:
    #             raise Exception("Function call returned empty content")
            
    #         if verbose:
    #             print(f"-> {result_message['content']}")
                
    # else:
    #     print(message.content)
    
    # return message

def run_chat_cli(client):
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument(
        "user_prompt",
        type=str,
        help="User prompt",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    run_agent(
        client,
        messages,
        verbose=args.verbose,
    )

def run_agent(client, messages, verbose:bool=False):
    for _ in range(20):

        message = call_llm_once(
            client,
            messages,
            verbose,
        )

        # Assistant message must be added first
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(
                    tool_call,
                    verbose=verbose,
                )

                if not result_message["content"]:
                    raise Exception(
                        "Function call returned empty content"
                    )

                # Then add each tool result
                messages.append(result_message)

                if verbose:
                    print(f"-> {result_message['content']}")

            # Go around loop again so model can see tool results
            continue

        # No tool calls means the model is finished
        print("Final response:")
        print(message.content)
        return

    print("Error: Maximum number of agent iterations reached.")



def main():
    load_dotenv()
    client = create_llm_client()
    run_chat_cli(client)



if __name__ == "__main__":

    # main_single_call()
    # main_agent_call()
    main()
