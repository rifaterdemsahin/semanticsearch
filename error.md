# Semantic Search Error Log

## Issue Identified
When querying the Qdrant database for `"turkish lady names"`, the system incorrectly returned Turkish male names (e.g., `İsmail`, `Ahmet`, `Ömer`, etc.) instead of the expected lady names:
- Ayse
- Suyehla
- Zeynep
- Zeliha
- Caroline

## Root Cause Analysis
1. **Context Collapse**: Bare names (e.g., "Ayse") as isolated strings lack explicit gender morphology in vector space. When queried with "turkish lady names", the phrase heavily associates with "turkish", retrieving the most common Turkish names in the dataset (which are predominantly male).
2. **Incorrect Source Data Structure**: In the raw `names.md` file, the female names (`Ayse`, `Zeynep`, etc.) were appended under the header `### Turkish Men's Names`. Even if the model had contextual extraction, the local context labeled them as men.
3. **Data Representation**: Vector databases do not magically add knowledge unless it is encoded in the textual representation fed to the embedder.

## The Fix
To natively support advanced semantic concepts like "lady names," the vector representations must contain entity context during ingestion:
1. **Restructure `names.md`**: Move the female names under correctly labeled headers (`### Turkish Women's Names` and `### English Women's Names`).
2. **Context Enriched Embedding**: Modify `load_names.py` so it parses the markdown headings. Instead of vectorizing just `"Ayse"`, it will vectorize `<NAME> - <CATEGORY>` (e.g., `"Ayse - Turkish Women's Names"`).
3. **Re-index & Re-test**: By embedding the category alongside the name, any query for `"lady names"` will strongly align with the `"Women's Names"` conceptual vectors, instantly mapping the correct subset.
