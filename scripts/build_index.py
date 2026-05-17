import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)


print("Loading catalog...")

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


documents = []

valid_items = []


for item in catalog:

    name = item.get("name", "")
    description = item.get("description", "")
    category = item.get("category", "")
    test_type = item.get("test_type", "")

    combined_text = f"""
    Assessment Name: {name}

    Description:
    {description}

    Category:
    {category}

    Test Type:
    {test_type}
    """

    combined_text = combined_text.strip()

    if len(combined_text) < 20:
        continue

    documents.append(combined_text)

    valid_items.append(item)


print(f"Creating embeddings for {len(documents)} items...")


embeddings = model.encode(
    documents,
    show_progress_bar=True,
    convert_to_numpy=True
)


embeddings = embeddings.astype("float32")


dimension = embeddings.shape[1]


print("Building FAISS index...")


index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


faiss.write_index(index, "data/faiss.index")


with open("data/clean_catalog.json", "w", encoding="utf-8") as f:
    json.dump(
        valid_items,
        f,
        indent=2,
        ensure_ascii=False
    )


print("\nFAISS index saved -> data/faiss.index")
print("Clean catalog saved -> data/clean_catalog.json")
print("DONE")