from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import os
import glob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Qdrant Client
QDRANT_URL = os.getenv("QDRANT_URL", "https://semantic-search-qdrant.fly.dev")
# Note: In production, you'd use a QDRANT_API_KEY
client = QdrantClient(QDRANT_URL, port=443)
COLLECTION_NAME = "repository_knowledge"

# Initialize Embedding Model
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
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
        # Check Qdrant connection
        collections = client.get_collections()
        return {"status": "connected", "qdrant": "ok", "model": MODEL_NAME}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/index")
async def trigger_indexing(background_tasks: BackgroundTasks):
    background_tasks.add_task(perform_indexing)
    return {"status": "indexing_started"}

def perform_indexing():
    # 1. Create collection if it doesn't exist
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=client.get_fastembed_vector_params()
        )

    # 2. Scan for markdown files
    files = glob.glob("**/*.md", recursive=True)
    points = []
    
    for idx, file_path in enumerate(files):
        if "_obsolete" in file_path or ".venv" in file_path:
            continue
            
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()
            if not content.strip():
                continue
                
            # Embed the content (take first 1000 chars for simplicity)
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

    # 3. Upsert to Qdrant
    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    print(f"Indexed {len(points)} files.")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
