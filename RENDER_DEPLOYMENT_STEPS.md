# Render.com Deployment - Step by Step Guide

## ✅ What's Already Done

- ✅ Code pushed to GitHub: https://github.com/kyluxj/civic-engagement-platform
- ✅ render.yaml configuration file created
- ✅ Build script created
- ✅ All backend code ready

---

## 🚀 Deploy Backend to Render.com (5 minutes)

### Step 1: Go to Render Dashboard

1. Open https://dashboard.render.com
2. Login with GitHub (you're already authorized)

### Step 2: Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### Step 3: Connect Repository

1. Click **"Connect account"** if needed (or it may already be connected)
2. Search for: **civic-engagement-platform**
3. Click **"Connect"** next to the repository

### Step 4: Configure Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `civic-platform-api` |
| **Region** | Oregon (US West) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn run:app` |
| **Instance Type** | `Free` |

### Step 5: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these 4 variables:

#### 1. DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: (Leave empty for now - we'll add after creating database)

#### 2. JWT_SECRET_KEY
- **Key**: `JWT_SECRET_KEY`
- **Value**: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2`
  
(Or generate a new one with: `python3 -c "import secrets; print(secrets.token_hex(32))"`)

#### 3. OPENAI_API_KEY
- **Key**: `OPENAI_API_KEY`
- **Value**: `YOUR_OPENAI_API_KEY_HERE`
  
(Get from: https://platform.openai.com/api-keys)

#### 4. FLASK_ENV
- **Key**: `FLASK_ENV`
- **Value**: `production`

#### 5. CORS_ORIGINS
- **Key**: `CORS_ORIGINS`
- **Value**: `https://civic-engagement-platform.netlify.app`

(Update this after you get your Netlify URL)

### Step 6: Create PostgreSQL Database

**BEFORE clicking "Create Web Service"**, we need to create the database:

1. Open a new tab
2. Go to https://dashboard.render.com
3. Click **"New +"** → **"PostgreSQL"**
4. Configure database:
   - **Name**: `civic-platform-db`
   - **Database**: `civic_platform`
   - **User**: `civic_user`
   - **Region**: Oregon (same as web service)
   - **Plan**: **Free**
5. Click **"Create Database"**
6. Wait 1-2 minutes for database to be created
7. **Copy the "Internal Database URL"** (it looks like: `postgresql://civic_user:...@...`)

### Step 7: Update DATABASE_URL

1. Go back to your Web Service configuration tab
2. Find the `DATABASE_URL` environment variable
3. Paste the Internal Database URL you just copied
4. Click **"Create Web Service"**

### Step 8: Wait for Deployment

- Deployment takes 3-5 minutes
- You'll see build logs in real-time
- Wait for "Live" status

### Step 9: Initialize Database

Once deployed:

1. Click on your service name
2. Click **"Shell"** tab (top right)
3. Run this command:
   ```bash
   python seed_data.py
   ```
4. Wait for "Database seeded successfully!" message

### Step 10: Get Your Backend URL

1. Your backend URL will be: `https://civic-platform-api.onrender.com`
2. Test it by visiting: `https://civic-platform-api.onrender.com/health`
3. You should see: `{"status":"healthy",...}`

---

## 📝 Environment Variables Summary

Here's a quick reference for all environment variables:

```
DATABASE_URL=postgresql://civic_user:PASSWORD@HOST/civic_platform
JWT_SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
OPENAI_API_KEY=sk-your-openai-api-key-here
FLASK_ENV=production
CORS_ORIGINS=https://civic-engagement-platform.netlify.app
```

---

## 🔧 After Backend is Deployed

### Update Frontend Environment Variable

1. Go to your Netlify site settings
2. Go to **"Site configuration"** → **"Environment variables"**
3. Update or add:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://civic-platform-api.onrender.com`
4. Click **"Save"**
5. Go to **"Deploys"** → **"Trigger deploy"** → **"Deploy site"**

### Update CORS in Backend

1. Go to Render dashboard → Your web service
2. Go to **"Environment"** tab
3. Find `CORS_ORIGINS`
4. Update to your actual Netlify URL (e.g., `https://your-site-name.netlify.app`)
5. Save (service will auto-redeploy)

---

## ✅ Testing Your Deployment

### Test Backend

```bash
# Health check
curl https://civic-platform-api.onrender.com/health

# Test login
curl -X POST https://civic-platform-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### Test Frontend

1. Go to your Netlify URL
2. Login with:
   - Email: `admin@example.com`
   - Password: `admin123`
3. Test all features:
   - Create a campaign
   - Request AI recommendation
   - View analytics

---

## 🎉 You're Done!

Your Civic Engagement Platform is now live!

- **Frontend**: https://your-site-name.netlify.app
- **Backend**: https://civic-platform-api.onrender.com
- **GitHub**: https://github.com/kyluxj/civic-engagement-platform

---

## 🆘 Troubleshooting

### Backend won't start
- Check build logs in Render dashboard
- Verify all environment variables are set
- Ensure DATABASE_URL is correct

### Database connection error
- Verify DATABASE_URL matches the Internal Database URL from Render
- Check database is running in Render dashboard
- Ensure database and web service are in the same region

### CORS errors
- Update CORS_ORIGINS to match your exact Netlify URL
- Include `https://` in the URL
- No trailing slash

### AI recommendations not working
- Verify OPENAI_API_KEY is set correctly
- Check OpenAI account has credits
- Review backend logs for errors

---

## 💰 Free Tier Limits

**Render Free Tier:**
- ✅ 750 hours/month
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ First request after sleep takes ~30 seconds
- ✅ Automatic HTTPS
- ✅ Automatic deployments

**PostgreSQL Free Tier:**
- ✅ 1 GB storage
- ✅ 97 hours/month runtime
- ⚠️ Expires after 90 days (backup your data!)

**To avoid sleep (Upgrade to $7/month):**
- No sleep
- Faster performance
- Better for production

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **GitHub Repo**: https://github.com/kyluxj/civic-engagement-platform

---

**Deployment prepared by Manus AI** 🤖

