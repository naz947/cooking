#!/bin/bash
# Setup script for local development

echo "🍳 Cooking Data Setup"
echo "===================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "   Please edit .env with your Telegram credentials:"
    echo "   - Get API_ID and API_HASH from https://my.telegram.org/apps"
    echo "   - Get GROUP_ID from your Telegram group"
    cat .env
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Telegram API credentials"
echo "2. Run: python export_topic.py"
echo "3. Run: python enrich_youtube.py"
echo "4. Run: python -m http.server 8000"
echo "5. Open http://localhost:8000"
