#!/bin/bash

# Civic Engagement Platform - GitHub Deployment Setup Script
# This script helps prepare your project for GitHub and Netlify deployment

echo "=========================================="
echo "Civic Engagement Platform Deployment Setup"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Initialize git repository
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Create .gitignore
echo "📝 Creating .gitignore file..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
instance/
*.db
*.sqlite

# Node
node_modules/
dist/
build/
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment variables
.env
backend/.env
frontend/.env
EOF
echo "✅ .gitignore created"

# Create netlify.toml for frontend
echo "📝 Creating netlify.toml for frontend..."
cat > frontend/netlify.toml << 'EOF'
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
EOF
echo "✅ netlify.toml created"

# Create Procfile for backend (if using Heroku)
echo "📝 Creating Procfile for backend..."
cat > backend/Procfile << 'EOF'
web: gunicorn run:app
EOF
echo "✅ Procfile created"

# Create runtime.txt for backend
echo "📝 Creating runtime.txt for backend..."
cat > backend/runtime.txt << 'EOF'
python-3.11.0
EOF
echo "✅ runtime.txt created"

# Generate JWT secret key
echo ""
echo "🔐 Generating JWT Secret Key..."
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
echo "Your JWT Secret Key: $JWT_SECRET"
echo ""
echo "⚠️  IMPORTANT: Save this key securely! You'll need it for deployment."
echo ""

# Add all files
echo "📦 Adding files to Git..."
git add .
echo "✅ Files added"

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    echo "ℹ️  No changes to commit"
else
    # Commit
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit: Civic Engagement Intelligence Platform"
    echo "✅ Initial commit created"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Create a GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Create a new repository (public or private)"
echo "   - DO NOT initialize with README"
echo ""
echo "2. Connect to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy Backend to Render.com:"
echo "   - Go to https://render.com"
echo "   - Create PostgreSQL database"
echo "   - Create Web Service from GitHub repo"
echo "   - Set environment variables:"
echo "     DATABASE_URL=<from Render PostgreSQL>"
echo "     JWT_SECRET_KEY=$JWT_SECRET"
echo "     OPENAI_API_KEY=<your OpenAI key>"
echo "     FLASK_ENV=production"
echo "     CORS_ORIGINS=https://your-app.netlify.app"
echo ""
echo "4. Deploy Frontend to Netlify:"
echo "   - Go to https://netlify.com"
echo "   - Import from GitHub"
echo "   - Base directory: frontend"
echo "   - Build command: npm run build"
echo "   - Publish directory: frontend/dist"
echo "   - Environment variable:"
echo "     VITE_API_BASE_URL=https://your-backend.onrender.com"
echo ""
echo "5. Initialize database:"
echo "   - In Render dashboard, open Shell"
echo "   - Run: python seed_data.py"
echo ""
echo "📚 For detailed instructions, see:"
echo "   - GITHUB_NETLIFY_DEPLOYMENT.md"
echo "   - DEPLOYMENT_GUIDE.md"
echo ""
echo "🎉 Good luck with your deployment!"
echo ""

