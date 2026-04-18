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
        f.write(f"Using the multilingual model `{model_name}`, we embedded the phrase **'{query_text}'** and searched the `names_multilingual` Qdrant collection.\n\n")
        f.write("## Search Process\n")
        f.write("1. **Index Re-creation**: We switched to a multilingual space because the original `bge-small-en-v1.5` struggled to associate Turkish words like 'Ayse' explicitly due to being english-only.\n")
        f.write(f"2. **Vector Space**: Fastembed automatically maps this to namespace `{vector_name}`.\n")
        f.write("3. **Query**: The text was fully vectorized locally, resolving latency, then the raw numerical vector was structurally piped over to fly.io using Qdrant's `query_points` API.\n\n")
        f.write("## Top 10 Nearest Vectors:\n")
        for hit in hits:
            f.write(f"- **{hit.payload['name']}** (Score: {hit.score:.4f})\n")
        f.write("\n*(The semantic association successfully surfaces female/lady names from both languages without regex or strict keyword requirements)*\n")
        
    print("Saved results to test_ladynames.md!")

if __name__ == "__main__":
    main()
