# 🚌 Tamil Nadu Private Omni Bus AI Chatbot (RAG)

An AI-powered chatbot for searching and recommending private omni buses across Tamil Nadu using **Retrieval-Augmented Generation (RAG)**, **FAISS Vector Database**, and **Sentence Transformers**.

---

##  Project Overview

The chatbot understands natural language queries and retrieves the most relevant private bus information using semantic search.

Instead of traditional keyword matching, the system converts user queries into vector embeddings and performs similarity search using a FAISS vector database.

---

## Features

- 🚌 AI-powered bus recommendation
- 🔍 Semantic Search
- 🤖 Retrieval-Augmented Generation (RAG)
- ⚡ FAISS Vector Database
- 📄 Sentence Transformer Embeddings
- 💰 Fare-based search
- 🛏️ Bus Type filtering
- 🗺️ Source & Destination search
- ⭐ Operator search
- 📍 Boarding & Dropping Point information
- 🎯 Natural Language Query Support
- 🌐 Interactive Gradio Web Interface

---

# 📊 Dataset Information

Dataset contains **1000+ Tamil Nadu Private Omni Bus records**.

Each record includes:

- Bus ID
- Operator
- Bus Name
- Source City
- Destination City
- Bus Type
- Departure Time
- Arrival Time
- Duration
- Distance
- Fare
- Boarding Point
- Dropping Point
- Total Seats
- Available Seats
- Amenities
- Running Days
- Rating

---

# 🗂️ Vector Database

This project uses **FAISS (Facebook AI Similarity Search)** as the vector database.

### Vector Files

| File | Description |
|------|-------------|
| **bus_index.faiss** | Stores vector embeddings for semantic similarity search |
| **documents.pkl** | Stores original bus information mapped to each vector |

### Vector Database Workflow

```text
Bus Dataset
      │
      ▼
Sentence Transformer
      │
Generate Embeddings
      │
      ▼
FAISS Vector Database
(bus_index.faiss)
      │
      ▼
documents.pkl
      │
      ▼
Semantic Search
      │
      ▼
Top-K Relevant Bus Results
```

The vector database allows users to search buses using natural language instead of exact keywords.

---

# 🤖 RAG Pipeline

```text
User Query
      │
      ▼
Sentence Transformer
      │
      ▼
Query Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Retrieve Relevant Documents
      │
      ▼
Generate AI Response
      │
      ▼
Display Bus Recommendation
```

---

# 🛠 Technology Stack

## Programming Language

- Python

## AI Technologies

- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- Semantic Search
- FAISS Vector Database

## Libraries

- Gradio
- Pandas
- NumPy
- FAISS
- Sentence Transformers
- Transformers
- Torch

## Dataset

- Custom Tamil Nadu Private Omni Bus Dataset

## Deployment

- Railway
- GitHub

---

# 📂 Project Structure

```text
Tamil-Nadu-Private-Omni-Bus-AI-Chatbot-RAG/

│
├── app.py
├── config.py
├── filter_engine.py
├── search_engine.py
├── requirements.txt
├── README.md
│
├── data/
│   └── bus_services.csv
│
└── vector_db/
    ├── bus_index.faiss
    └── documents.pkl
```

---

# 🔍 Sample Queries

```
Chennai to Madurai

Bus from Coimbatore to Chennai

Luxury Sleeper Bus

Volvo Bus

Bus under ₹1000

GreenLine Travels

AC Bus

Bus with Available Seats

Bus from Salem to Chennai
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/sugumarranganathan/Tamil-Nadu-Private-Omni-Bus-AI-Chatbot-RAG.git
```

Go to the project folder

```bash
cd Tamil-Nadu-Private-Omni-Bus-AI-Chatbot-RAG
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

# 🌐 Deployment

This project can be deployed on

- Railway
- Hugging Face Spaces
- Render
- Koyeb
- Fly.io

---

# 📈 Project Highlights

- ✅ 1000+ Bus Records
- ✅ Semantic Search
- ✅ Sentence Transformer Embeddings
- ✅ FAISS Vector Database
- ✅ RAG Architecture
- ✅ Interactive Gradio Interface
- ✅ Railway Deployment Ready
- ✅ Open Source Project

---

# 🔮 Future Enhancements

- Online Bus Booking
- Live Seat Availability
- Bus Fare Prediction
- Voice Search
- Tamil Language Support
- AI Travel Assistant
- LLM Integration (Gemini/OpenAI)
- Live Bus Tracking

---

# 👨‍💻 Deverloped by

**Sugumar R**
