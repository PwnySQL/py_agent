import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

import prompts
from agent_functions import available_functions, call_function


def load_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Cannot load gemini api key!")
    return api_key


def query_gemini(
    prompt: str, messages: list, *, api_key: str = "", verbose: bool = False
):
    client = genai.Client(api_key=api_key)
    messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

    gen_content_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=prompts.system_prompt
        ),
    )

    if gen_content_response.usage_metadata is None:
        raise RuntimeError("Cannot access gemini response metadata! API call failed")
    usage_metadata = gen_content_response.usage_metadata

    # candidates are responses to the last prompt (usually one)
    if gen_content_response.candidates is not None:
        for cand in gen_content_response.candidates:
            # Remember answers and tool requests and ... from the model to form
            # a history which is passed to the model for the next iteration
            # such that it knows what it has done to infer what to do next.
            messages.append(cand.content)

    response = ""
    function_call_responses = []
    if gen_content_response.function_calls is not None:
        for call in gen_content_response.function_calls:
            function_call_result = call_function(call, verbose=verbose)
            if not function_call_result.parts:
                raise RuntimeError(
                    "Function call result must have a non-empty parts list"
                )
            if not function_call_result.parts[0].function_response:
                raise RuntimeError(
                    "First part of function call result must have a not-None function response"
                )
            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError(
                    "First function response must have a not-None response"
                )

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            function_call_responses.append(function_call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_call_responses))

    else:
        response = f"Response: {gen_content_response.text}"

    return usage_metadata, response


def parse_args():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    api_key = load_api_key()
    messages = []
    # Agent loop
    for _ in range(20):
        usage_metadata, response = query_gemini(
            args.user_prompt,
            messages,
            api_key=api_key,
            verbose=args.verbose,
        )
        if args.verbose:
            print(
                f"User prompt: {args.user_prompt}\n"
                f"Prompt tokens: {usage_metadata.prompt_token_count}\n"
                f"Response tokens: {usage_metadata.candidates_token_count}"
            )
        if response:
            # User query is answered
            print(response)
            return
    print(
        "Aborted! No response from LLM reached in maximum number of agent iterations."
    )
    exit(1)


if __name__ == "__main__":
    main()
