---
title: SHL Recommender System
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: streamlit
python_version: 3.11.9
app_file: app.py
sdk_version: 1.51.0
---

# SHL Recommender System

This project implements a recommender system that processes user queries and returns relevant recommendations.  
It provides both a **Streamlit interface** for interactive exploration and can be adapted to expose a **FastAPI backend**.

## 🚀 Features
- Text preprocessing (tokenization, embeddings, TF‑IDF).
- Hybrid recommendation scoring (semantic + keyword).
- Interactive Streamlit dashboard.
- Deployable via Docker or Hugging Face Spaces.

## 📦 How to Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py