# Environment Variables for Deployment

## Backend Environment Variables (Render.com)

Copy and paste these into Render when creating your web service:

### 1. DATABASE_URL
```
[Get from Render PostgreSQL after creating database]
```
**How to get:**
1. Create PostgreSQL database in Render
2. Copy "Internal Database URL" from database dashboard
3. Paste here

### 2. JWT_SECRET_KEY
```
561d91b1e1eeed691a221f594db5bf78721625f06fb1f89e8ea528e6b5b290b2
```
**Note:** This is a securely generated random key for JWT token encryption

### 3. OPENAI_API_KEY
```
[YOUR_OPENAI_API_KEY]
```
**How to get:**
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste here

### 4. FLASK_ENV
```
production
```

### 5. CORS_ORIGINS
```
https://civic-engagement-platform.netlify.app
```
**Note:** Update this with your actual Netlify URL after deployment

---

## Frontend Environment Variables (Netlify)

Add this in Netlify site settings:

### VITE_API_BASE_URL
```
https://civic-platform-api.onrender.com
```
**Note:** Update with your actual Render backend URL after deployment

---

## Quick Copy-Paste Format

### For Render Backend:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `[From Render PostgreSQL]` |
| `JWT_SECRET_KEY` | `561d91b1e1eeed691a221f594db5bf78721625f06fb1f89e8ea528e6b5b290b2` |
| `OPENAI_API_KEY` | `[Your OpenAI Key]` |
| `FLASK_ENV` | `production` |
| `CORS_ORIGINS` | `https://civic-engagement-platform.netlify.app` |

### For Netlify Frontend:

| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | `https://civic-platform-api.onrender.com` |

---

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` files to GitHub
- Keep these values secure
- Rotate JWT_SECRET_KEY periodically
- Protect your OpenAI API key

✅ **These values are already in .gitignore**

