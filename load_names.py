import re
from qdrant_client import QdrantClient

def main():
    print("Connecting to Qdrant...")
    client = QdrantClient("https://semantic-search-qdrant.fly.dev", port=443)
    
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    print(f"Setting multilingual model: {model_name}")
    client.set_model(model_name)
    
    print("Reading names.md...")
    with open("names.md", "r", encoding="utf-8") as f:
        text = f.read()

    names = []
    for line in text.split("\n"):
        match = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if match:
            names.append(match.group(1).strip())
            
    print(f"Found {len(names)} names.")
    metadata = [{"name": name} for name in names]
    
    # We must explicitly recreate to clear old models
    client.recreate_collection(
        collection_name="names_multilingual",
        vectors_config=client.get_fastembed_vector_params()
    )
    
    print("Uploading to Qdrant using multilingual model...")
    client.add(
        collection_name="names_multilingual",
        documents=names,
        metadata=metadata
    )
    print("Finished uploading!")

if __name__ == "__main__":
    main()
