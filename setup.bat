@echo off
echo ================================================
echo AI Policy Analyzer - Setup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama not found. Please install Ollama from https://ollama.ai
    echo.
)

echo ================================================
echo Setting up Backend...
echo ================================================
cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Check if PDFs exist
if not exist "data\pdfs\*.pdf" (
    echo.
    echo NOTE: No PDFs found in backend/data/pdfs/
    echo Please download the 21 PDFs from Google Drive and place them in backend/data/pdfs/
    echo Then run: python ingest.py
    pause
)

cd ..

echo.
echo ================================================
echo Setting up Frontend...
echo ================================================
cd frontend

REM Install Node dependencies
echo Installing Node dependencies...
call npm install

cd ..

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Download PDFs from Google Drive to backend/data/pdfs/
echo 2. Run: cd backend && python ingest.py (from venv)
echo 3. Start backend: python main.py
echo 4. Start frontend: cd frontend && npm run dev
echo.
pause
