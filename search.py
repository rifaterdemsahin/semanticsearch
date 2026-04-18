from fastembed import TextEmbedding
from qdrant_client import QdrantClient

def main():
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    print(f"Generating multilingual embedding for 'turkish lady names' using {model_name}...")
    model = TextEmbedding(model_name)
    
    query_text = "turkish lady names"
    vector = next(model.embed([query_text])).tolist()

    client = QdrantClient("https://semantic-search-qdrant.fly.dev", port=443)
    client.set_model(model_name)
    
    vector_name = list(client.get_fastembed_vector_params().keys())[0]
    print(f"Querying Qdrant using vector namespace: {vector_name}...")
    
    hits = client.query_points(
        collection_name="names_multilingual",
        query=vector,
        using=vector_name,
        limit=10
    ).points

    print(f"Search results for '{query_text}':")
    for hit in hits:
        print(f"- {hit.payload['name']} (score: {hit.score:.4f})")
        
    with open("test_ladynames.md", "w") as f:
        f.write("# Semantic Search Results: Lady Names\n\n")
        f.write(f"Using the contextual enriched models and `{model_name}`, we successfully queried **'{query_text}'**.\n\n")
        f.write("## The Fix Process\n")
        f.write("To correctly capture lady names, we fixed `names.md` heavily mis-structured data, and synthetically enriched vectors during load (e.g. `Ayse is in the category of Turkish Women's Names`).\n\n")
        f.write("## Top Results:\n")
        for hit in hits:
            f.write(f"- **{hit.payload['name']}** (Origin: {hit.payload['category']}, Score: {hit.score:.4f})\n")
        
    print("Saved results to test_ladynames.md!")

if __name__ == "__main__":
    main()
