FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY 5_Symbols/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project for indexing (excluding via .dockerignore)
COPY . .

EXPOSE 8000

# Run uvicorn pointing to the backend module in 5_Symbols
CMD ["uvicorn", "5_Symbols.backend:app", "--host", "0.0.0.0", "--port", "8000"]
