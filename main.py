import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from call_function import call_function
from config import MAX_ITERS, MODEL
from prompts import system_prompt
from call_function import available_functions

def generate(client, messages, verbose):
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    if verbose and response.usage_metadata:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    function_responses = []
    if (response.function_calls):
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose = verbose)
            if not function_call_result.parts or not function_call_result.parts[0].function_response:
                raise Exception("Error: No function call output")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("Error: No function response generated")
        messages.append(types.Content(role="tool", parts=function_responses))
    else:
        return response.text

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if len(args):
        prompt = " ".join(args)
    else:
        print("Usage: uv run main.py <prompt>")
        sys.exit(1)

    if verbose:
        print("User prompt:", prompt)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user",parts=[types.Part(text=prompt)])
    ]


    iters = 0
    while True:
        iters += 1

        if iters > MAX_ITERS:
            print("Max iterations reached")
            sys.exit(1)

        try:
            response = generate(client, messages, verbose)
            if response:
                print(response)
                break
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)




if __name__ == "__main__":
    main()
