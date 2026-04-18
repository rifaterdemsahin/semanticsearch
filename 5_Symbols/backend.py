from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import os
import glob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

QDRANT_URL = os.getenv("QDRANT_URL", "https://semantic-search-qdrant.fly.dev")
client = QdrantClient(QDRANT_URL, port=443)
COLLECTION_NAME = "repository_knowledge"

MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_SIZE = 384
model = TextEmbedding(MODEL_NAME)

@app.get("/search")
async def search(q: str):
    vector = next(model.embed([q])).tolist()
    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=10
    ).points
    return hits

@app.get("/check_connection")
async def check_connection():
    try:
        collections = client.get_collections()
        return {"status": "connected", "qdrant": "ok", "model": MODEL_NAME}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/index")
async def trigger_indexing(background_tasks: BackgroundTasks):
    background_tasks.add_task(perform_indexing)
    return {"status": "indexing_started"}

def perform_indexing():
    # Recreate collection with explicit vector params (384-dim bge-small-en-v1.5)
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in collections:
        client.delete_collection(COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )

    files = glob.glob("**/*.md", recursive=True)
    points = []

    for idx, file_path in enumerate(files):
        if "_obsolete" in file_path or ".venv" in file_path:
            continue
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()
            if not content.strip():
                continue
            snippet = content[:1000]
            vector = next(model.embed([snippet])).tolist()
            points.append(PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "path": file_path,
                    "name": os.path.basename(file_path),
                    "snippet": snippet[:200]
                }
            ))

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)

    print(f"Indexed {len(points)} files.")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
