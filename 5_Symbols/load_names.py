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
    metadata = []
    current_category = "Unknown"
    
    for line in text.split("\n"):
        line = line.strip()
        # Track active markdown heading
        header_match = re.match(r"^#+\s+(.+)$", line)
        if header_match:
            current_category = header_match.group(1).strip()
            continue
            
        name_match = re.match(r"^\d+\.\s+(.+)$", line)
        if name_match:
            raw_name = name_match.group(1).strip()
            # Context substitution: embed "Ayse (Turkish Women's Names)"
            enriched_context = f"{raw_name} is in the category of {current_category}"
            names.append(enriched_context)
            metadata.append({"name": raw_name, "category": current_category})
            
    print(f"Found {len(names)} names.")
    
    client.recreate_collection(
        collection_name="names_multilingual",
        vectors_config=client.get_fastembed_vector_params()
    )
    
    print("Uploading to Qdrant using context-enriched models...")
    client.add(
        collection_name="names_multilingual",
        documents=names,
        metadata=metadata
    )
    print("Finished uploading!")

if __name__ == "__main__":
    main()
