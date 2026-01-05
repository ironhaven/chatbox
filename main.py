import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt

from functions import get_files_info, write_file, get_file_content, run_python_file


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


messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
output = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt,
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

if output.function_calls is not None:
    print("function call:")
    for function_call in output.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print("text:")
    print(output.text)
