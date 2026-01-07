import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt

from functions import get_files_info, write_file, get_file_content, run_python_file, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY env var not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = genai.Client(api_key=api_key)
available_functions = types.Tool(
    function_declarations=[get_files_info.schema_get_files_info,
                           get_file_content.schema_get_file_content,
                           write_file.schema_write_file,
                           run_python_file.schema_run_python_file],
)


def generate_content(client, messages, available_function):
    output = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, tools=[available_functions]
            )
            
    )
    metadata = output.usage_metadata
    prompt_tokens = metadata.prompt_token_count
    resp_tokens = metadata.candidates_token_count

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", resp_tokens)

    return output





messages = []
messages.append(types.Content(role="user", parts=[types.Part(text=args.user_prompt)]))
if args.verbose:
    print("User prompt:", args.user_prompt)


# loop until you get a text response from llm
for i in range(20):
    if args.verbose:
        print(f"loop {i}: {len(messages)}")
    output = generate_content(client, messages, available_functions)
    for candidate in output.candidates:
        messages.append(candidate.content)

    if output.function_calls:
        print("function call:")
        results = []
        for function_call_n in output.function_calls:
            call_result = call_function.call_function(function_call_n, args.verbose)
            if not call_result.parts:
                raise Exception("Empty Function call parts")
            if call_result.parts[0].function_response is None:
                raise Exception("None function_response")
            if call_result.parts[0].function_response.response is None:
                raise Exception("None function_response.response")
            if args.verbose:
                print(f"-> {call_result.parts[0].function_response.response}")
            results.append(call_result.parts[0])

        messages.append(types.Content(role="user", parts=results))


    else:
        print("text:")
        print(output.text)
        break
else:
    print("Maximum loops reached")

