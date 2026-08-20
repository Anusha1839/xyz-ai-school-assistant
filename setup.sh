#!/bin/bash

# XYZ AI School Assistant - Setup Script
# Supports: macOS, Linux, Windows (Git Bash/WSL)

set -e

echo "🤖 XYZ AI School Assistant - Setup"
echo "===================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ Pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Create directories
echo "📂 Creating directories..."
mkdir -p .streamlit
echo "✓ Directories created"
echo ""

# Check if secrets.toml exists
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  .streamlit/secrets.toml not found"
    echo "📋 Creating template file..."
    cat > .streamlit/secrets.toml << 'EOF'
# Add your Gemini API key here
# Get your API key from: https://makersuite.google.com/app/apikey
gemini_api_key = "YOUR_GEMINI_API_KEY_HERE"
EOF
    echo "✓ Template created at .streamlit/secrets.toml"
    echo ""
    echo "⚠️  IMPORTANT: Update .streamlit/secrets.toml with your Gemini API key"
    echo "   Get your free key at: https://makersuite.google.com/app/apikey"
else
    echo "✓ .streamlit/secrets.toml already exists"
fi
echo ""

# Display instructions
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add your Gemini API key to .streamlit/secrets.toml"
echo "2. Run: streamlit run app.py"
echo "3. Try demo credentials:"
echo "   - Email: student@school.com"
echo "   - Password: student123"
echo ""
echo "📚 For more info, see README.md"
echo ""
