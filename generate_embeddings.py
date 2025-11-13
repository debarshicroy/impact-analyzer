from sentence_transformers import SentenceTransformer
import chromadb
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="system_artifacts")

for folder in ['data/requirements', 'data/design', 'data/code_docs', 'data/test_cases']:
    for file in os.listdir(folder):
        path = f"{folder}/{file}"
        with open(path, "r") as f:
            content = f.read()
            embedding = model.encode(content).tolist()
            collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[{"file_name": file, "path": path}]
            )
print("✅ Embeddings generated and stored in local ChromaDB.")
