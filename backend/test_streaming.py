from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)

client = Groq()

print("Testing Groq streaming format...\n")

stream = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say 'Hello world' in 2 words"}],
    stream=True,
    max_tokens=20
)

print("Stream type:", type(stream))
print("Stream:", stream)
print("\nIterating through stream:\n")

for i, chunk in enumerate(stream):
    print(f"Chunk {i}:")
    print(f"  Type: {type(chunk)}")
    print(f"  Has choices: {hasattr(chunk, 'choices')}")

    if hasattr(chunk, 'choices') and chunk.choices:
        choice = chunk.choices[0]
        print(f"  Choice type: {type(choice)}")
        print(f"  Choice delta: {choice.delta}")
        if hasattr(choice.delta, 'content'):
            print(f"  Content: {choice.delta.content}")

    if i >= 2:
        print("\n... (showing first 3 chunks)")
        break

print("\nDone!")
