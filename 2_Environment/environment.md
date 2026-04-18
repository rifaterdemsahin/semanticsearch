# Environment Setup and Implementation Log

This document tracks the timeline and technical steps taken to construct the `semanticsearch` project with Doppler and Qdrant on Fly.io.

## Steps Completed

### 1. Initial Data Pipeline

- Created `test_dataset_names.md`, containing a dataset of 20 English male names and 20 Turkish male names.
- Committed and pushed this foundational dataset to the remote repository.

### 2. Secret Management with Doppler

- Installed the Doppler CLI (`brew install dopplerhq/cli/doppler` / explicit installation).
- Successfully initialized a new Doppler project named `semanticsearch`.
- Saved the existing `FlyV1` deployment API key securely as the `FLY_API_TOKEN` Doppler secret.
- Linked the local working directory to Doppler's `dev` environment for automatic secret injection (`doppler setup`).

### 3. Deploying Qdrant on Fly.io

- Utilized Doppler-injected credentials to provision a new Fly.io application named `semantic-search-qdrant`.
- Created an encrypted 1GB volume named `qdrant_data` in the `ams` region to allow Qdrant to persist its embedded vectors.
- Established a local directory named `qdrant` and generated a `fly.toml` configuration targeting the `qdrant/qdrant:latest` Docker image.
- Deployed Qdrant to a Fly.io v2 Machine via `flyctl deploy`.
- Confirmed the instance was publicly accessible and healthy at `https://semantic-search-qdrant.fly.dev/`.

### 4. Vectorizing and Populating the Database

- Deployed a Python 3 isolated virtual environment (`.venv`).
- Installed `qdrant-client` paired with `fastembed` (an officially supported lightweight embedding provider).
- Developed a loader script (`load_names.py`) to scrape the raw contents of `names.md`.
- Converted all 42 extracted names into fixed-dimensional vectors using the BAAI semantic embedding model (`bge-small-en-v1.5`).
- Uploaded vectors and raw metadata into a new Qdrant namespace named `names_collection`.

### 5. Executing Semantic Search

- Created an inference query script (`search.py`) leveraging the unified `fastembed` TextEmbedding instance.
- Executed querying against the phrase `"lady names"` to demonstrate the power of semantic matching across diverse domains.
