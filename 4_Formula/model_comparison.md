# Semantic Search Pipeline: Embedding Models Comparison

During the development and debugging of the `semanticsearch` project, we downloaded and tested multiple embedding models to calculate vectors that accurately represented our queries. 

Below is a detailed comparison of the models interacting closely with our Turkish/English dataset.

## FastEmbed Model Capabilities Table

| Model Name | Size | Dimensions | Language Support | Use-Case in Project | Performance & Observations |
|---|---|---|---|---|---|
| **`BAAI/bge-small-en-v1.5`** | ~133 MB | 384 | English Only | Initial pipeline setup & trial run. | Extremely fast. However, it severely misjudged "turkish lady names" because it lacks native Turkish training representations. |
| **`paraphrase-multilingual-MiniLM-L12-v2`** | ~471 MB | 384 | Multilingual (50+) | First attempt at multilingual reindexing. | Sufficient syntax handling, but failed the zero-shot semantic gender logic. It succumbed to *"context collapse"*, meaning it over-indexed on the word "Turkish" and ignored "lady", returning common Turkish male names (`Mustafa`, `Ismail`). |
| **`intfloat/multilingual-e5-large`** | ~2.24 GB | 1024| Multilingual | Attempted robust semantic grouping. | Exceptional theoretical performance, however, the massive 2.24GB file size proved severely inefficient for local ingestion scripts. The download sequence was manually aborted. |
| **`paraphrase-multilingual-mpnet-base-v2`** | ~1.13 GB | 768 | Multilingual (50+) | Final deployed model coupled with enriched data. | The *"Goldilocks"* model for our stack. It's an expansive base structure without the bloat of large parameter counts. When supplied with parsed `"Name is in the category of..."` text, it perfectly distributed vectors, scoring target female names natively between **`0.73 - 0.78`**. |

## Summary of Findings
1. **Size vs Capability**: The `MiniLM` models are incredibly powerful for raw string-to-string similarity but lack the deep conceptual associations required to dynamically evaluate gender out of raw vocabulary. Stepping up to a `base` parameter length like `MPNet` provides the necessary nuance.
2. **Language Thresholds**: Testing Turkish semantic values on English-optimized tools (`bge-small-en`) will reliably result in linguistic noise. Always align the pipeline natively.
3. **The Importance of Context**: Regardless of the Model size, text-embedding engines perform exponentially better when isolated strings are mathematically expanded into complete logical sequences (context-aware strings) before vectorization occurs.
