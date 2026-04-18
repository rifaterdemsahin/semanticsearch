# Semantic Search Error Log

## Issue Identified
When using the model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` to query `"turkish lady names"`, the top results mistakenly surfaced male names heavily (e.g., `Mustafa` was the top result).

## Expected Results
The model should have correctly associated the semantic concept of a "lady" with the actual female names present in the dataset:
- Ayse
- Suyehla
- Zeynep
- Zeliha
- Caroline

## Root Cause Analysis
1. **Model Capability**: The `MiniLM-L12` model is compact and lightweight, designed for basic paraphrasing and similarity. It lacks the deep, rich conceptual encoding required to intuitively link the isolated single-word string `"Ayse"` with the descriptive phrase `"turkish lady names"` without additional context.
2. **Context Absence**: Since we are only feeding raw names (e.g., "Ayse") into the vector database rather than a descriptive phrase (e.g., "Ayse is a Turkish female name"), the model relies heavily on its internal pre-trained biases to map the vector for the name directly to the vector for the concept "lady names".

## Proposed Fix
1. **Switch to a Large-Scale, Robust Multilingual Model**: We will step up to `intfloat/multilingual-e5-large`. E5-Large is a heavily tuned sentence transformer explicitly designed to bridge the gap between queries and conceptually related passages using powerful zero-shot associations.
2. **Re-index and Re-test**: We will re-embed the list with `intfloat/multilingual-e5-large` into a new collection and explicitly test if it can recover the female names from the raw list.
