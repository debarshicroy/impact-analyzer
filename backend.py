from sentence_transformers import SentenceTransformer
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.get_collection("system_artifacts")

# Either use OpenAI or local Ollama model
USE_OLLAMA = False  # set True if you want local model
if not USE_OLLAMA:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_llm(prompt: str):
    if USE_OLLAMA:
        import subprocess, json
        result = subprocess.run(["ollama", "run", "mistral", prompt], capture_output=True, text=True)
        return result.stdout.strip()
    else:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

def analyze_impact(requirement_text: str):
    # Step 1: Find related artifacts
    req_embedding = model.encode(requirement_text).tolist()
    results = collection.query(query_embeddings=[req_embedding], n_results=5)

    related_docs = "\n\n".join(results["documents"][0])
    prompt = f"""
    You are a senior system analyst. Analyze the new requirement and find what could be impacted.
    Return a JSON object in this format:
    {{
        "impacted_modules": [],
        "impacted_tests": [],
        "risk_level": "",
        "summary": "",
        "suggested_actions": []
    }}

    Requirement:
    {requirement_text}

    Related system documents:
    {related_docs}
    """

    result = query_llm(prompt)
    try:
        data = json.loads(result)
    except:
        data = {"summary": result}
    return data
