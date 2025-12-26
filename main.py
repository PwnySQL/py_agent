import os
from dotenv import load_dotenv
from google import genai


def load_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Cannot load gemini api key!")
    return api_key


def query_gemini(content: str, *, api_key=""):
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content,
    )
    if resp.usage_metadata is None:
        raise RuntimeError("Cannot access gemini response metadata! API call failed")
    usage_metadata = resp.usage_metadata
    return usage_metadata, resp.text


def main():
    api_key = load_api_key()
    usage_metadata, response = query_gemini(
        "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        api_key=api_key,
    )
    print(
        f"Prompt tokens: {usage_metadata.prompt_token_count}\n"
        f"Response tokens: {usage_metadata.candidates_token_count}"
    )
    print(f"Response: {response}")


if __name__ == "__main__":
    main()
