import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Unable to find API Key")
client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Tux2 Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    v = args.verbose
    if v:
        print(f"User prompt: {args.user_prompt}")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )
        if len(response.candidates) > 0:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.usage_metadata == None:
            raise RuntimeError("Unable to contact Gemini")
        if v:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        function_results = []
        if response.function_calls != None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, v)
                if len(function_call_result.parts) <= 0:
                    raise Exception(f"No parts in function call result: {function_call_result}")
                if not isinstance(function_call_result.parts[0].function_response, types.FunctionResponse):
                    raise Exception(f"Function Response is not a type.FunctionResponse: {function_call_result}")
                function_results.append(function_call_result.parts[0])
                if v:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            exit(0)
    print("Unable to find a solution! Exiting...")
    exit(1)

if __name__ == "__main__":
    main()
