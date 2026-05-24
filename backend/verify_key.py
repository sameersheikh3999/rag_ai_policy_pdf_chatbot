from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key: {api_key[:20]}...\n")

print("Testing available Groq models...\n")

# Try more models
models = [
    "llama-3.3-70b-versatile",
    "llama-3.3-70b-specdec",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "qwq-32b-preview",
]

client = Groq()

for model in models:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5,
        )
        print(f"[SUCCESS] Model: {model}")
        print(f"Response: {response.choices[0].message.content}\n")
        break
    except Exception as e:
        error = str(e)
        if "not found" in error.lower() or "404" in error:
            print(f"[NOT FOUND] {model}")
        elif "decommissioned" in error.lower():
            print(f"[DEPRECATED] {model}")
        else:
            print(f"[ERROR] {model}")
            print(f"  {error[:80]}\n")
