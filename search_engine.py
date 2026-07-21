"""
=========================================================
part 1 Hybrid Search Engine
Tamil Nadu Private Omni Bus AI Chatbot (RAG)

Version : 3.0
Author  : Sugumar R
=========================================================
"""

# ==========================================================
# Imports
# ==========================================================

import pickle
import faiss
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer

from config import (
    DATA_FILE,
    INDEX_FILE,
    CHUNKS_FILE,
    MODEL_NAME
)

from filter_engine import filter_dataframe

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip()

# ==========================================================
# Load Embedding Model
# ==========================================================

print("=" * 60)
print("Loading Sentence Transformer...")
print("=" * 60)

model = SentenceTransformer(MODEL_NAME)

# ==========================================================
# Load FAISS Index
# ==========================================================

print("=" * 60)
print("Loading FAISS Index...")
print("=" * 60)

index = faiss.read_index(INDEX_FILE)

# ==========================================================
# Load Documents
# ==========================================================

print("=" * 60)
print("Loading Documents...")
print("=" * 60)

with open(CHUNKS_FILE, "rb") as f:
    documents = pickle.load(f)

print(f"Loaded {len(documents)} documents")

# ==========================================================
# Configuration
# ==========================================================

TOP_K = 50

MAX_RESULTS = 5

CONFIDENCE_THRESHOLD = 30

# ==========================================================
# Confidence Score
# ==========================================================

def confidence(distance):

    score = 1 / (1 + float(distance))

    return round(score * 100, 2)

# ==========================================================
# Format Search Result
# ==========================================================

def format_result(row, score):

    return f"""
🚌 Operator : {row['Operator']}

🪑 Bus : {row['Bus_Name']}

🚍 Type : {row['Bus_Type']}

⭐ Rating : {row['Rating']}

📍 Route : {row['From_City']} ➜ {row['To_City']}

🕒 Departure : {row['Departure_Time']}

🕒 Arrival : {row['Arrival_Time']}

⏳ Duration : {row['Duration']}

💰 Fare : ₹{row['Fare']}

💺 Available Seats : {row['Available_Seats']}

📌 Boarding : {row['Boarding_Point']}

📌 Dropping : {row['Dropping_Point']}

🎁 Amenities : {row['Amenities']}

🆔 Bus ID : {row['Bus_ID']}

✅ Confidence : {score}%
"""

# part 2

# ==========================================================
# Find Bus ID from Document
# ==========================================================

def find_bus_id(document):
    """
    Extract Bus_ID from a document chunk.
    """

    for line in document.split("\n"):

        if line.startswith("Bus_ID"):

            try:
                return line.split(":", 1)[1].strip()
            except IndexError:
                return None

    return None


# ==========================================================
# Hybrid AI Search
# ==========================================================

def ai_search(query):

    # ------------------------------------------------------
    # Stage 1 : Structured Filtering
    # ------------------------------------------------------

    filtered_df, filters = filter_dataframe(query)

    if filtered_df.empty:

        return "❌ No buses found matching your criteria."

    # ------------------------------------------------------
    # Stage 2 : Query Embedding
    # ------------------------------------------------------

    embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype(np.float32)

    top_k = min(TOP_K, index.ntotal)

    distances, indices = index.search(
        embedding,
        top_k
    )

    # ------------------------------------------------------
    # Stage 3 : Candidate Ranking
    # ------------------------------------------------------

    filtered_bus_ids = set(
        filtered_df["Bus_ID"].astype(str)
    )

    results = []

    seen_bus_ids = set()

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx == -1:
            continue

        document = documents[idx]

        bus_id = find_bus_id(document)

        if bus_id is None:
            continue

        if bus_id not in filtered_bus_ids:
            continue

        if bus_id in seen_bus_ids:
            continue

        rows = filtered_df[
            filtered_df["Bus_ID"].astype(str) == bus_id
        ]

        if rows.empty:
            continue

        row = rows.iloc[0]

        score = confidence(distance)

        if score < CONFIDENCE_THRESHOLD:
            continue

        results.append(

            {

                "bus_id": bus_id,

                "score": score,

                "distance": float(distance),

                "row": row

            }

        )

        seen_bus_ids.add(bus_id)

    # ------------------------------------------------------
    # Stage 4 : Fallback
    # ------------------------------------------------------

    if len(results) == 0:

        for _, row in filtered_df.head(MAX_RESULTS).iterrows():

            results.append(

                {

                    "bus_id": str(row["Bus_ID"]),

                    "score": 50,

                    "distance": 999,

                    "row": row

                }

            )

    # ------------------------------------------------------
    # Stage 5 : Sort by Confidence
    # ------------------------------------------------------

    results = sorted(

        results,

        key=lambda x: x["score"],

        reverse=True

    )

    # ------------------------------------------------------
    # Stage 6 : Generate Response
    # ------------------------------------------------------

    answer = "# 🚌 Search Results\n\n"

    answer += f"Found {len(results)} matching buses.\n\n"

    for i, result in enumerate(results[:MAX_RESULTS], start=1):

        answer += f"## {i}\n\n"

        answer += format_result(

            result["row"],

            result["score"]

        )

        answer += "\n"

    return answer

# part 3

# ==========================================================
# Search Statistics
# ==========================================================

def search_statistics():

    return {

        "total_documents": len(documents),

        "total_vectors": index.ntotal,

        "embedding_model": MODEL_NAME,

        "dataset_records": len(df)

    }


# ==========================================================
# Pretty Print Statistics
# ==========================================================

def print_statistics():

    stats = search_statistics()

    print("=" * 60)

    print("Hybrid AI Search Engine")

    print("=" * 60)

    print(f"Dataset Records : {stats['dataset_records']}")

    print(f"Vector Records  : {stats['total_vectors']}")

    print(f"Documents       : {stats['total_documents']}")

    print(f"Embedding Model : {stats['embedding_model']}")

    print("=" * 60)


# ==========================================================
# Health Check
# ==========================================================

def health_check():

    try:

        assert len(documents) > 0

        assert index.ntotal > 0

        assert len(df) > 0

        print("✅ Search Engine Ready")

        return True

    except Exception as e:

        print("❌ Search Engine Error")

        print(e)

        return False


# ==========================================================
# Safe Search Wrapper
# ==========================================================

def search(query):

    try:

        if query is None:

            return "Please enter a question."

        query = str(query).strip()

        if len(query) == 0:

            return "Please enter a question."

        return ai_search(query)

    except Exception as e:

        return f"Search Error : {str(e)}"


# ==========================================================
# Startup
# ==========================================================

print_statistics()

health_check()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    while True:

        query = input("\nAsk : ")

        if query.lower() in [

            "exit",

            "quit",

            "bye"

        ]:

            break

        print()

        print(search(query))



