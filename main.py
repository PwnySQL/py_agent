import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Cannot load gemini api key!")
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )
    if resp.usage_metadata is None:
        raise RuntimeError("Cannot access gemini response metadata! API call failed")
    print(
        f"Prompt tokens: {resp.usage_metadata.prompt_token_count}\n"
        f"Response tokens: {resp.usage_metadata.candidates_token_count}"
    )
    print(f"Response: {resp.text}")


if __name__ == "__main__":
    main()
