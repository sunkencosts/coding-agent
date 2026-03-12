import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
def main():
    print("Hello from coding-agent!")

    if api_key is None:
        raise RuntimeError("API_KEY not found")

    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    if not response.text and not response.usage_metadata:
        raise RuntimeError("Did not get good LLM response")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
