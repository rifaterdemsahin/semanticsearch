from qdrant_client import QdrantClient

from fastembed import TextEmbedding

def main():
    print("Generating embedding for 'lady names'...")
    model = TextEmbedding("BAAI/bge-small-en-v1.5")
    vector = next(model.embed(["lady names"])).tolist()

    client = QdrantClient("https://semantic-search-qdrant.fly.dev", port=443)
    
    print("Querying Qdrant...")
    hits = client.query_points(
        collection_name="names_collection",
        query=vector,
        using="fast-bge-small-en",
        limit=5
    ).points

    print("Search results for 'lady names':")
    for hit in hits:
        print(f"- {hit.payload['name']} (score: {hit.score:.4f})")

if __name__ == "__main__":
    main()
