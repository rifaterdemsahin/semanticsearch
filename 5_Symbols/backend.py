from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Qdrant Client
QDRANT_URL = os.getenv("QDRANT_URL", "https://semantic-search-qdrant.fly.dev")
client = QdrantClient(QDRANT_URL, port=443)

# Initialize Embedding Model
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
model = TextEmbedding(MODEL_NAME)

@app.get("/search")
async def search(q: str):
    # Embed the query
    vector = next(model.embed([q])).tolist()
    
    # Query Qdrant
    hits = client.query_points(
        collection_name="names_multilingual",
        query=vector,
        limit=10
    ).points
    
    return hits

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
