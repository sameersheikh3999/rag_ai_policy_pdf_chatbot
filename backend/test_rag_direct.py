from dotenv import load_dotenv
load_dotenv(override=True)

from rag_pipeline import RAGPipeline
import os

print(f"API Key from env: {os.getenv('GROQ_API_KEY')[:20]}...")

print("Initializing RAG Pipeline...")
try:
    rag = RAGPipeline()
    print("RAG Pipeline initialized successfully!")

    print("\nTesting generate_response with streaming...")
    stream = rag.generate_response("Test context about education", "What is education?", use_streaming=True)

    print(f"Stream type: {type(stream)}")

    print("Getting first chunk...")
    for i, chunk in enumerate(stream):
        if i == 0:
            print(f"First chunk type: {type(chunk)}")
            if hasattr(chunk, 'choices'):
                print(f"Has choices: True")
                if chunk.choices and len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    print(f"First content: {content}")
            break

    print("Stream test successful!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
