#!/bin/bash

echo "Starting AI Chatbot Application..."
echo ""

echo "1. Checking for Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi

echo "2. Installing required packages..."
pip install -r requirements.txt

echo "3. Starting Streamlit app..."
echo ""
echo "Access the chatbot at http://localhost:8501"
echo ""
streamlit run app.py 