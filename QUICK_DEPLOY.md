# Quick Deploy Reference Card

## 🚀 Deploy in 15 Minutes

### Prerequisites
- GitHub account
- Netlify account (free)
- Render.com account (free)
- OpenAI API key

---

## Step 1: GitHub (2 minutes)

```bash
# Run setup script
./deploy-setup.sh

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/civic-platform.git
git push -u origin main
```

---

## Step 2: Backend - Render.com (5 minutes)

### A. Create Database
1. Go to https://render.com → New → PostgreSQL
2. Name: `civic-platform-db`
3. Plan: Free
4. **Copy Internal Database URL**

### B. Deploy Backend
1. New → Web Service
2. Connect GitHub repo
3. Settings:
   - Name: `civic-platform-api`
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn run:app`
4. Environment Variables:
   ```
   DATABASE_URL=<paste from database>
   JWT_SECRET_KEY=<generate with: python3 -c "import secrets; print(secrets.token_hex(32))">
   OPENAI_API_KEY=sk-your-key
   FLASK_ENV=production
   CORS_ORIGINS=https://your-app.netlify.app
   ```
5. Create Web Service
6. **Copy your backend URL**: `https://civic-platform-api.onrender.com`

### C. Initialize Database
1. In Render dashboard → Shell
2. Run: `python seed_data.py`

---

## Step 3: Frontend - Netlify (3 minutes)

1. Go to https://netlify.com → Add new site → Import from Git
2. Connect GitHub → Select repo
3. Settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
4. Environment Variables:
   ```
   VITE_API_BASE_URL=https://civic-platform-api.onrender.com
   ```
5. Deploy site
6. **Copy your frontend URL**: `https://your-app.netlify.app`

---

## Step 4: Update CORS (1 minute)

1. Go back to Render → Your backend service
2. Environment → Edit `CORS_ORIGINS`
3. Change to: `https://your-app.netlify.app`
4. Save (auto-redeploys)

---

## Step 5: Test (2 minutes)

1. Open your Netlify URL
2. Login:
   - Email: `admin@example.com`
   - Password: `admin123`
3. ✅ Change password immediately!
4. Test creating a campaign
5. Test AI recommendation

---

## 🎉 Done!

Your platform is live at:
- **Frontend**: https://your-app.netlify.app
- **Backend**: https://civic-platform-api.onrender.com

---

## Troubleshooting

**Can't login?**
- Check backend logs in Render
- Verify DATABASE_URL is correct
- Ensure seed_data.py ran successfully

**CORS error?**
- Update CORS_ORIGINS in Render
- Must match exact Netlify URL (with https://)

**AI not working?**
- Verify OPENAI_API_KEY in Render
- Check OpenAI account has credits

---

## Free Tier Limits

**Render Free:**
- Sleeps after 15 min inactivity
- 750 hours/month
- First request after sleep is slow (~30 seconds)

**Netlify Free:**
- 100 GB bandwidth/month
- 300 build minutes/month
- Perfect for this app

**Upgrade for Production:**
- Render: $7/month (no sleep)
- Database: $7/month (more storage)
- Total: $14/month

---

## Environment Variables Quick Reference

### Backend (Render)
| Variable | Get From |
|----------|----------|
| `DATABASE_URL` | Render PostgreSQL dashboard |
| `JWT_SECRET_KEY` | Generate: `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| `FLASK_ENV` | Set to: `production` |
| `CORS_ORIGINS` | Your Netlify URL |

### Frontend (Netlify)
| Variable | Get From |
|----------|----------|
| `VITE_API_BASE_URL` | Your Render backend URL |

---

## Useful Commands

```bash
# View backend logs
# Go to Render dashboard → Logs tab

# Redeploy backend
# Render dashboard → Manual Deploy → Deploy latest commit

# Redeploy frontend
# Netlify dashboard → Deploys → Trigger deploy

# Rollback frontend
# Netlify dashboard → Deploys → Find old deploy → Publish

# Access database
# Render dashboard → Database → Connect
```

---

## Custom Domain (Optional)

### Netlify
1. Domain settings → Add custom domain
2. Update DNS records at your registrar
3. SSL auto-configured

### Render
1. Settings → Custom Domain
2. Add domain
3. Update DNS CNAME record

---

## Next Steps

1. ✅ Change default admin password
2. ✅ Create your organization
3. ✅ Add team members
4. ✅ Create first campaign
5. ✅ Request AI recommendations
6. ✅ Monitor analytics

---

## Support

- **Full Guide**: GITHUB_NETLIFY_DEPLOYMENT.md
- **Render Docs**: https://render.com/docs
- **Netlify Docs**: https://docs.netlify.com

---

**Deployment Time**: ~15 minutes  
**Cost**: $0 (free tier) or $14/month (production)  
**Difficulty**: Easy ⭐⭐☆☆☆

