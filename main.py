import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

import prompts


def load_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Cannot load gemini api key!")
    return api_key


def query_gemini(prompt: str, messages: list, *, api_key=""):
    client = genai.Client(api_key=api_key)
    messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=prompts.system_prompt),
    )
    if resp.usage_metadata is None:
        raise RuntimeError("Cannot access gemini response metadata! API call failed")
    usage_metadata = resp.usage_metadata
    return usage_metadata, resp.text


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
    usage_metadata, response = query_gemini(
        args.user_prompt,
        messages,
        api_key=api_key,
    )
    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\n"
            f"Prompt tokens: {usage_metadata.prompt_token_count}\n"
            f"Response tokens: {usage_metadata.candidates_token_count}"
        )
    print(f"Response: {response}")


if __name__ == "__main__":
    main()
