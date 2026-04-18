# semanticsearch
Semantic Search implementation using Qdrant deployed on Fly.io.

## Overview
This project demonstrates setting up a scalable vector search pipeline. We have:
1. Created an initial dataset (`names.md`) of varying names.
2. Secured deployment credentials using **Doppler**.
3. Deployed a persistent **Qdrant** database on **Fly.io** (`semantic-search-qdrant`).
4. Used `fastembed` with the `BAAI/bge-small-en-v1.5` embeddings model to vectorize the names and insert them into the database.

## Results of the Semantic Search
When extracting the top vectors matching the concept of **"lady names"** using our python query script (`search.py`), the Qdrant vector database yielded the following semantic proximity results:
- Caroline (score: 0.6944)
- William (score: 0.6705)
- George (score: 0.6657)
- Christopher (score: 0.6657)
- Charles (score: 0.6552)

*(See `environment.md` for a full breakdown of the environment deployment steps)*
