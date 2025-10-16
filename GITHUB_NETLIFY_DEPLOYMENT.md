# GitHub + Netlify Deployment Guide

This guide provides step-by-step instructions for deploying the Civic Engagement Intelligence Platform using GitHub for version control and Netlify for frontend hosting.

## Deployment Architecture

**Frontend:** Netlify (Free tier available)  
**Backend:** Render.com or Railway.app (Free tier available)  
**Database:** PostgreSQL on Render/Railway or Supabase  
**Version Control:** GitHub

---

## Part 1: GitHub Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub** (https://github.com)
2. **Create a new repository:**
   - Click the "+" icon in the top right
   - Select "New repository"
   - Repository name: `civic-engagement-platform`
   - Description: "Civic Engagement Intelligence Platform with AI-powered recommendations"
   - Choose "Private" or "Public" based on your needs
   - **Do NOT** initialize with README (we already have one)
   - Click "Create repository"

### Step 2: Prepare Your Local Repository

```bash
# Navigate to the project directory
cd /path/to/civic-platform

# Initialize git (if not already initialized)
git init

# Create .gitignore file
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
EOF

# Add all files
git add .

# Commit
git commit -m "Initial commit: Civic Engagement Intelligence Platform"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/civic-engagement-platform.git

# Push to GitHub
git push -u origin main
```

### Step 3: Create Separate Branches (Optional but Recommended)

```bash
# Create development branch
git checkout -b development
git push -u origin development

# Create staging branch
git checkout -b staging
git push -u origin staging

# Return to main
git checkout main
```

**Branch Strategy:**
- `main` - Production-ready code
- `staging` - Pre-production testing
- `development` - Active development

---

## Part 2: Backend Deployment (Render.com)

### Why Render.com?
- Free tier available
- Easy PostgreSQL database setup
- Automatic deployments from GitHub
- Built-in SSL certificates
- Environment variable management

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 2: Create PostgreSQL Database

1. **Click "New +"** → **"PostgreSQL"**
2. **Configure database:**
   - Name: `civic-platform-db`
   - Database: `civic_platform`
   - User: `civic_user`
   - Region: Choose closest to your users
   - Plan: **Free** (or paid for production)
3. **Click "Create Database"**
4. **Save the connection details:**
   - Internal Database URL (for backend)
   - External Database URL (for local development)

### Step 3: Deploy Backend to Render

1. **Click "New +"** → **"Web Service"**

2. **Connect Repository:**
   - Select your GitHub repository
   - Choose the repository: `civic-engagement-platform`

3. **Configure Service:**
   - Name: `civic-platform-api`
   - Region: Same as database
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
   - Plan: **Free** (or paid for production)

4. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"

   ```
   DATABASE_URL = [Paste Internal Database URL from Step 2]
   JWT_SECRET_KEY = [Generate a secure random key]
   OPENAI_API_KEY = [Your OpenAI API key]
   FLASK_ENV = production
   CORS_ORIGINS = https://your-app-name.netlify.app
   ```

   **To generate JWT_SECRET_KEY:**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Click "Create Web Service"**

6. **Wait for deployment** (5-10 minutes)

7. **Note your backend URL:** `https://civic-platform-api.onrender.com`

### Step 4: Initialize Database

1. **Go to your Render service**
2. **Click "Shell"** (in the top right)
3. **Run initialization:**
   ```bash
   python seed_data.py
   ```

---

## Part 3: Frontend Deployment (Netlify)

### Step 1: Prepare Frontend for Deployment

1. **Update frontend configuration:**

   Create `frontend/netlify.toml`:
   ```toml
   [build]
     command = "npm run build"
     publish = "dist"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200

   [build.environment]
     NODE_VERSION = "18"
   ```

2. **Update API URL in frontend:**

   Edit `frontend/.env`:
   ```
   VITE_API_BASE_URL=https://civic-platform-api.onrender.com
   ```

3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Configure for Netlify deployment"
   git push origin main
   ```

### Step 2: Deploy to Netlify

**Option A: Deploy via Netlify Dashboard (Recommended)**

1. **Go to Netlify** (https://netlify.com)
2. **Sign up/Login** with GitHub
3. **Click "Add new site"** → **"Import an existing project"**
4. **Connect to GitHub:**
   - Authorize Netlify
   - Select your repository: `civic-engagement-platform`
5. **Configure build settings:**
   - Branch to deploy: `main`
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
6. **Add environment variables:**
   - Click "Show advanced"
   - Add variable:
     - Key: `VITE_API_BASE_URL`
     - Value: `https://civic-platform-api.onrender.com`
7. **Click "Deploy site"**
8. **Wait for deployment** (2-5 minutes)

**Option B: Deploy via Netlify CLI**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Navigate to frontend directory
cd frontend

# Build the project
npm run build

# Deploy
netlify deploy --prod

# Follow the prompts:
# - Create & configure a new site
# - Choose your team
# - Site name: civic-engagement-platform
# - Publish directory: dist
```

### Step 3: Configure Custom Domain (Optional)

1. **In Netlify Dashboard:**
   - Go to "Site settings" → "Domain management"
   - Click "Add custom domain"
   - Enter your domain: `civicplatform.com`
   - Follow DNS configuration instructions

2. **Enable HTTPS:**
   - Netlify automatically provisions SSL certificate
   - Usually takes 1-2 minutes

### Step 4: Update Backend CORS

1. **Go to Render Dashboard**
2. **Select your backend service**
3. **Go to "Environment"**
4. **Update CORS_ORIGINS:**
   ```
   CORS_ORIGINS = https://your-site-name.netlify.app
   ```
   Or with custom domain:
   ```
   CORS_ORIGINS = https://civicplatform.com
   ```
5. **Save changes** (service will redeploy automatically)

---

## Part 4: Continuous Deployment Setup

### Automatic Deployments

Both Render and Netlify support automatic deployments from GitHub:

**Backend (Render):**
- Automatically deploys when you push to `main` branch
- Build logs available in Render dashboard
- Rollback available if deployment fails

**Frontend (Netlify):**
- Automatically deploys when you push to `main` branch
- Deploy previews for pull requests
- Instant rollback to previous deployments

### Deployment Workflow

```bash
# Make changes locally
git checkout development
# ... make your changes ...

# Commit and push to development
git add .
git commit -m "Add new feature"
git push origin development

# Test on development environment (if configured)

# Merge to staging for testing
git checkout staging
git merge development
git push origin staging

# After testing, merge to main for production
git checkout main
git merge staging
git push origin main

# Both Render and Netlify will automatically deploy!
```

---

## Part 5: Environment Variables Reference

### Backend Environment Variables (Render)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | `64-character-hex-string` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `FLASK_ENV` | Flask environment | `production` |
| `CORS_ORIGINS` | Allowed frontend origins | `https://app.netlify.app` |

### Frontend Environment Variables (Netlify)

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `https://api.onrender.com` |

---

## Part 6: Testing Your Deployment

### 1. Test Backend API

```bash
# Health check
curl https://civic-platform-api.onrender.com/health

# Expected response:
# {"status":"healthy","service":"Civic Engagement Intelligence Platform API"}

# Test login
curl -X POST https://civic-platform-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### 2. Test Frontend

1. **Open your Netlify URL** in a browser
2. **Test login:**
   - Email: `admin@example.com`
   - Password: `admin123`
3. **Verify all pages load:**
   - Dashboard
   - Users
   - Organizations
   - Campaigns
   - AI Agents
   - Analytics
4. **Test creating a campaign**
5. **Test requesting an AI recommendation**

### 3. Test Integration

1. **Create a new user** in the Users page
2. **Create an organization**
3. **Create a campaign** for that organization
4. **Request an AI recommendation** for the campaign
5. **Review the recommendation**
6. **Check analytics** to see data updates

---

## Part 7: Monitoring and Maintenance

### Render Monitoring

**View Logs:**
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. View real-time logs

**Monitor Performance:**
1. Click "Metrics" tab
2. View CPU, Memory, and Request metrics
3. Set up alerts for downtime

### Netlify Monitoring

**View Deploy Logs:**
1. Go to Netlify Dashboard
2. Select your site
3. Click "Deploys"
4. Click on any deploy to see logs

**Analytics:**
1. Click "Analytics" tab
2. View visitor statistics
3. Monitor bandwidth usage

### Database Backups

**Render PostgreSQL:**
1. Automatic daily backups on paid plans
2. Manual backups: Dashboard → Database → "Backups"
3. Download backup files for local storage

---

## Part 8: Troubleshooting

### Common Issues

**Issue: Frontend can't connect to backend**

**Solution:**
1. Check CORS_ORIGINS in backend environment variables
2. Verify VITE_API_BASE_URL in frontend
3. Check browser console for CORS errors
4. Ensure backend is deployed and running

**Issue: Database connection failed**

**Solution:**
1. Verify DATABASE_URL is correct
2. Check database is running in Render
3. Ensure database allows connections from backend
4. Review backend logs for specific error

**Issue: Build failed on Netlify**

**Solution:**
1. Check build logs in Netlify dashboard
2. Verify package.json has correct dependencies
3. Ensure Node version is compatible (18+)
4. Check for syntax errors in code

**Issue: AI recommendations not working**

**Solution:**
1. Verify OPENAI_API_KEY is set correctly
2. Check OpenAI API quota and billing
3. Review backend logs for API errors
4. Test API key with curl:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

**Issue: Slow backend response**

**Solution:**
1. Upgrade to paid Render plan (free tier sleeps after inactivity)
2. Optimize database queries
3. Add caching layer
4. Consider using CDN for static assets

---

## Part 9: Cost Breakdown

### Free Tier Limits

**Render.com Free Tier:**
- 750 hours/month of runtime
- Sleeps after 15 minutes of inactivity
- 512 MB RAM
- PostgreSQL: 1GB storage, 97 hours/month

**Netlify Free Tier:**
- 100 GB bandwidth/month
- 300 build minutes/month
- Unlimited sites
- Automatic SSL

**Estimated Costs for Production:**

| Service | Free Tier | Paid Tier | Recommended |
|---------|-----------|-----------|-------------|
| Render Backend | $0 | $7/month | Paid for production |
| Render Database | $0 | $7/month | Paid for production |
| Netlify Frontend | $0 | $19/month | Free is fine |
| **Total** | **$0** | **$14-33/month** | **$14/month minimum** |

---

## Part 10: Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` files to GitHub
- ✅ Use different keys for development and production
- ✅ Rotate JWT secret keys periodically
- ✅ Keep OpenAI API keys secure

### 2. Database Security
- ✅ Use strong database passwords
- ✅ Enable SSL for database connections
- ✅ Restrict database access to backend only
- ✅ Regular backups

### 3. API Security
- ✅ Enable rate limiting
- ✅ Use HTTPS only
- ✅ Implement proper CORS configuration
- ✅ Keep dependencies updated

### 4. Monitoring
- ✅ Set up error tracking (Sentry)
- ✅ Monitor API usage
- ✅ Track failed login attempts
- ✅ Review audit logs regularly

---

## Part 11: Updating Your Deployment

### Making Changes

```bash
# 1. Make changes locally
git checkout development
# ... edit files ...

# 2. Test locally
cd backend && python run.py
cd frontend && npm run dev

# 3. Commit changes
git add .
git commit -m "Description of changes"
git push origin development

# 4. Merge to main when ready
git checkout main
git merge development
git push origin main

# 5. Automatic deployment happens!
# - Render deploys backend
# - Netlify deploys frontend
```

### Rolling Back

**Netlify:**
1. Go to "Deploys"
2. Find previous working deploy
3. Click "..." → "Publish deploy"

**Render:**
1. Go to service dashboard
2. Click "Manual Deploy"
3. Select previous commit
4. Click "Deploy"

---

## Part 12: Alternative Backend Options

### Option 1: Railway.app (Alternative to Render)

**Advantages:**
- Similar to Render
- Generous free tier
- Easy PostgreSQL setup

**Setup:**
1. Go to https://railway.app
2. Connect GitHub repository
3. Add PostgreSQL database
4. Deploy backend service
5. Configure environment variables

### Option 2: Heroku

**Advantages:**
- Well-established platform
- Extensive documentation
- Many add-ons available

**Setup:**
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
cd backend
heroku create civic-platform-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set JWT_SECRET_KEY="your-key"
heroku config:set OPENAI_API_KEY="your-key"

# Deploy
git push heroku main
```

### Option 3: Vercel (Alternative to Netlify)

**For Frontend:**
1. Go to https://vercel.com
2. Import GitHub repository
3. Configure:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add environment variable: `VITE_API_BASE_URL`
5. Deploy

---

## Summary Checklist

- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Deploy PostgreSQL database on Render
- [ ] Deploy backend to Render
- [ ] Initialize database with seed data
- [ ] Create Netlify account
- [ ] Deploy frontend to Netlify
- [ ] Configure environment variables
- [ ] Update CORS settings
- [ ] Test login and basic functionality
- [ ] Test AI recommendations
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring and alerts
- [ ] Document deployment for team

---

## Support Resources

**Render Documentation:** https://render.com/docs  
**Netlify Documentation:** https://docs.netlify.com  
**GitHub Documentation:** https://docs.github.com

**Need Help?**
- Render Community: https://community.render.com
- Netlify Community: https://answers.netlify.com
- GitHub Discussions: In your repository

---

**Your deployment is now complete! 🎉**

Your Civic Engagement Intelligence Platform is now live and accessible worldwide with automatic deployments from GitHub!

