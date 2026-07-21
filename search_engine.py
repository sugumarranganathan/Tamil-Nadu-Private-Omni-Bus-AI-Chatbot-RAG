import pickle
import faiss
from sentence_transformers import SentenceTransformer
from config import MODEL_NAME, INDEX_FILE, CHUNKS_FILE

model = SentenceTransformer(MODEL_NAME)

index = faiss.read_index(INDEX_FILE)

with open(CHUNKS_FILE, "rb") as f:
    documents = pickle.load(f)


def ai_search(query):

    embedding = model.encode([query])

    distances, indices = index.search(embedding, 5)

    response = ""

    for rank, idx in enumerate(indices[0], start=1):

        if idx == -1:
            continue

        response += f"### Result {rank}\n"
        response += documents[idx]
        response += "\n\n"

    return response
