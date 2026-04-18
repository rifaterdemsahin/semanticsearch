import os
import re
from qdrant_client import QdrantClient

def main():
    print("Connecting to Qdrant...")
    client = QdrantClient("https://semantic-search-qdrant.fly.dev", port=443)
    
    print("Reading names.md...")
    with open("names.md", "r", encoding="utf-8") as f:
        text = f.read()

    # Extract names matching pattern "1. Name"
    names = []
    for line in text.split("\n"):
        match = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if match:
            names.append(match.group(1).strip())
            
    print(f"Found {len(names)} names.")
    
    metadata = [{"name": name} for name in names]
    
    print("Uploading to Qdrant (this will also generate embeddings)...")
    # This automatically downloads the fastembed model, creates the collection, embeds and uploads
    client.add(
        collection_name="names_collection",
        documents=names,
        metadata=metadata
    )
    print("Finished uploading!")

if __name__ == "__main__":
    main()
