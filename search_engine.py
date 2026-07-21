import faiss
import pickle
from sentence_transformers import SentenceTransformer
from config import MODEL_NAME, INDEX_FILE, CHUNKS_FILE

# Load embedding model
model = SentenceTransformer(MODEL_NAME)

# Load FAISS index
index = faiss.read_index(INDEX_FILE)

# Load chunks
with open(CHUNKS_FILE, "rb") as f:
    documents = pickle.load(f)
