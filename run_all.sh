#!/bin/bash
# 1. Start FastAPI Backend in background and log output
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
echo "🚀 Backend started on port 8000"

# 2. Start Streamlit Frontend
streamlit run frontend/app.py