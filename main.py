import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    print("Hello from coding-agent!")

    if api_key is None:
        raise RuntimeError("API_KEY not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    function_results = []
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if len(response.candidates):
            for c in response.candidates:
                messages.append(c.content)

        if not response.text and not response.usage_metadata:
            raise RuntimeError("Did not get good LLM response")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, args.verbose)

            if len(function_call_result.parts) == 0:
                raise Exception("no parts")
            if function_call_result.parts[0].function_response == None:
                raise Exception("no function response")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("no response")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
    print("Something went wrong")
    sys.exit(1)


if __name__ == "__main__":
    main()
