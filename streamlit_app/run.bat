@echo off
echo Starting AI Chatbot Application...
echo.
echo 1. Checking for Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

echo 2. Checking for required packages...
pip install -r requirements.txt

echo 3. Starting Streamlit app...
echo.
echo Access the chatbot at http://localhost:8501
echo.
streamlit run app.py

pause 