# Semantic Search: The "Context Collapse" Fix

This document explains the technical pivot used to solve the semantic routing failure, where searching for `"turkish lady names"` mistakenly surfaced male names heavily instead of the desired female names.

## 1. The Problem Space (Context Collapse)
In vector mathematics, embedding an isolated name like `"Ayse"` places the vector purely based on the general dataset distribution of the word "Ayse". Without additional descriptors, vectors for single proper nouns struggle to link with rich, descriptive query strings like `"turkish lady names"`. 

The model (`mpnet-base`) primarily recognized the anchor word **Turkish** in the query and matched it to the dominant cluster of Turkish vectors in Qdrant, which happened to be the 20 male names (Ahmet, Ismail, etc.).

Furthermore, investigating the source file (`names.md`) revealed that the names Ayse, Zeynep, Suyehla, and Zeliha were inadvertently appended under the heading `### Turkish Men's Names`.

## 2. The Solution (Semantic Enrichment at Ingestion)
The fix required moving away from embedding "raw data" to embedding "contextualized data". You cannot search for a semantic attribute if the attribute isn't mapped to the vector.

Here is how we resolved it:

### Step A: Data Restructuring
We fixed the source `names.md` file by inserting correct hierarchical headings:
- `### Turkish Women's Names` (Ayse, Suyehla, Zeynep, Zeliha)
- `### English Women's Names` (Caroline)

### Step B: The Code Fix (`load_names.py`)
Instead of blindly looping through lines and embedding only the name, I updated the ingestion script to dynamically parse the active Markdown heading. 

**Before (Raw String Embedding):**
```python
names.append(raw_name) # Vectorizing: "Ayse"
```

**After (Context-Enriched Embedding):**
```python
enriched_context = f"{raw_name} is in the category of {current_category}"
names.append(enriched_context) # Vectorizing: "Ayse is in the category of Turkish Women's Names"
```

By passing this synthesized descriptive string to the embedding model (`sentence-transformers/paraphrase-multilingual-mpnet-base-v2`), we forced the vector representations separating into explicit gender and language clusters.

## 3. The Result
Because the vector database now holds representations of explicit contextual statements rather than disconnected nouns, querying `"turkish lady names"` instantly mapped successfully to the newly established "Turkish Women's Names" cluster space.

**Final Precision Scores:**
- **Ayse** (Score: 0.7825) - *(Massive leap from noise)*
- **Zeliha** (Score: 0.7485)
- **Suyehla** (Score: 0.7405)
- **Zeynep** (Score: 0.7345)
