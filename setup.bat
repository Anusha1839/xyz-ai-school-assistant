@echo off
REM XYZ AI School Assistant - Setup Script for Windows

echo.
echo 🤖 XYZ AI School Assistant - Setup
echo ====================================
echo.

REM Check Python
echo ✓ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✓ Pip upgraded
echo.

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt --quiet
echo ✓ Dependencies installed
echo.

REM Create directories
echo 📂 Creating directories...
if not exist ".streamlit" mkdir .streamlit
echo ✓ Directories created
echo.

REM Check if secrets.toml exists
if not exist ".streamlit\secrets.toml" (
    echo ⚠️  .streamlit\secrets.toml not found
    echo 📋 Creating template file...
    (
        echo # Add your Gemini API key here
        echo # Get your API key from: https://makersuite.google.com/app/apikey
        echo gemini_api_key = "YOUR_GEMINI_API_KEY_HERE"
    ) > .streamlit\secrets.toml
    echo ✓ Template created at .streamlit\secrets.toml
    echo.
    echo ⚠️  IMPORTANT: Update .streamlit\secrets.toml with your Gemini API key
    echo    Get your free key at: https://makersuite.google.com/app/apikey
) else (
    echo ✓ .streamlit\secrets.toml already exists
)
echo.

REM Display instructions
echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Add your Gemini API key to .streamlit\secrets.toml
echo 2. Run: streamlit run app.py
echo 3. Try demo credentials:
echo    - Email: student@school.com
echo    - Password: student123
echo.
echo 📚 For more info, see README.md
echo.

pause
