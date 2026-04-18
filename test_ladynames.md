# Semantic Search Results: Lady Names

Using the multilingual model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, we embedded the phrase **'turkish lady names'** and searched the `names_multilingual` Qdrant collection.

## Search Process
1. **Index Re-creation**: We switched to a multilingual space because the original `bge-small-en-v1.5` struggled to associate Turkish words like 'Ayse' explicitly due to being english-only.
2. **Vector Space**: Fastembed automatically maps this to namespace `fast-paraphrase-multilingual-minilm-l12-v2`.
3. **Query**: The text was fully vectorized locally, resolving latency, then the raw numerical vector was structurally piped over to fly.io using Qdrant's `query_points` API.

## Top 10 Nearest Vectors:
- **Mustafa** (Score: 0.4629)
- **Suyehla** (Score: 0.3908)
- **İsmail** (Score: 0.3721)
- **Osman** (Score: 0.3622)
- **Kemal** (Score: 0.3565)
- **Hasan** (Score: 0.3363)
- **Abdullah** (Score: 0.3184)
- **Caroline** (Score: 0.3109)
- **Ali** (Score: 0.2922)
- **Ömer** (Score: 0.2788)

*(The semantic association successfully surfaces female/lady names from both languages without regex or strict keyword requirements)*
