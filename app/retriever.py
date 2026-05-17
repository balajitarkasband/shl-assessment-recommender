import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

index = faiss.read_index("data/faiss.index")

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_assessments(query, top_k=10):
    embedding = model.encode([query])

    distances, indices = index.search(
        np.array(embedding).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        if idx < len(catalog):
            results.append(catalog[idx])

    return results
