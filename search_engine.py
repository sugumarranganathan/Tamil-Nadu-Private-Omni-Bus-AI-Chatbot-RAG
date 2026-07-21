# Step 1 — Import filter_engine

import pandas as pd
import numpy as np
import faiss
import pickle

from sentence_transformers import SentenceTransformer

from config import *

from filter_engine import filter_dataframe

# Step 2 — Create Document Mapping
# After loading documents.pkl

# ==========================================================
# Document Lookup
# ==========================================================

document_lookup = {}

for doc in documents:

    bus_id = None

    lines = doc.split("\n")

    for line in lines:

        if "Bus_ID" in line:

            bus_id = line.split(":")[1].strip()

            break

    if bus_id:

        document_lookup[bus_id] = doc

# Step 3 — Confidence Score

# ==========================================================
# Confidence
# ==========================================================

def confidence(distance):

    score = 1 / (1 + distance)

    return round(score * 100, 2)


# Step 4 — Format Result

def format_result(row, score):

    return f"""
🚌 {row['Operator']}

⭐ Rating : {row['Rating']}

📍 Route : {row['From_City']} ➜ {row['To_City']}

🪑 Bus : {row['Bus_Name']}

🚍 Type : {row['Bus_Type']}

🕒 Departure : {row['Departure_Time']}

🕒 Arrival : {row['Arrival_Time']}

💰 Fare : ₹{row['Fare']}

💺 Seats : {row['Available_Seats']}

📌 Boarding : {row['Boarding_Point']}

📌 Dropping : {row['Dropping_Point']}

🎁 Amenities : {row['Amenities']}

✅ Confidence : {score}%
"""

# Step 5 — Hybrid AI Search

def ai_search(query):

    # ----------------------------------------
    # Stage 1 : Structured Filtering
    # ----------------------------------------

    filtered_df, filters = filter_dataframe(query)

    if filtered_df.empty:

        return "❌ No buses found matching your criteria."

    # ----------------------------------------
    # Stage 2 : Semantic Search
    # ----------------------------------------

    embedding = model.encode([query])

    distances, indices = index.search(embedding, 20)

    results = []

    filtered_bus_ids = set(filtered_df["Bus_ID"].astype(str))

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        doc = documents[idx]

        bus_id = None

        for line in doc.split("\n"):

            if "Bus_ID" in line:

                bus_id = line.split(":")[1].strip()

                break

        if bus_id not in filtered_bus_ids:

            continue

        row = filtered_df[
            filtered_df["Bus_ID"].astype(str) == bus_id
        ].iloc[0]

        results.append(

            (

                confidence(distance),

                format_result(

                    row,

                    confidence(distance)

                )

            )

        )

    if not results:

        return "❌ No matching buses found."

    results.sort(

        reverse=True,

        key=lambda x: x[0]

    )

    answer = "# 🚌 Search Results\n\n"

    for i, (_, text) in enumerate(results[:5], start=1):

        answer += f"## {i}\n"

        answer += text

        answer += "\n"

    return answer



