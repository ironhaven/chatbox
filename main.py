import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY env var not found")

client = genai.Client(api_key=api_key)
output = client.models.generate_content(model="gemini-2.5-flash",
                                        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

metadata = output.usage_metadata
prompt_tokens = metadata.prompt_token_count
resp_tokens = metadata.candidates_token_count
print("Prompt tokens:", prompt_tokens)
print("Response tokens:", resp_tokens)
print("Response:")
print(output.text)
