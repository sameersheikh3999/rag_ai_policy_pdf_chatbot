# Deployment Guide - Railway

This guide walks you through deploying the AI Policy Analyzer on Railway.

## Prerequisites

1. **GitHub Account** - Push your code to GitHub
2. **Railway Account** - Sign up at https://railway.app
3. **Groq API Key** - From https://console.groq.com/

---

## Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)
```bash
cd AI_Policy_Analyzer_Tool
git init
git add .
git commit -m "Initial commit: AI Policy Analyzer"
```

### 1.2 Create `.gitignore`
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env
.env.local

# Node
node_modules/
dist/
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Data
data/pdfs/*.pdf
data/faiss_index/
```

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/AI_Policy_Analyzer_Tool.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend on Railway

### 2.1 Create Railway Project
1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub"
4. Connect your GitHub account
5. Select the `AI_Policy_Analyzer_Tool` repository

### 2.2 Configure Backend Service

#### Build Settings:
- **Base Directory**: `backend`
- **Python Version**: `3.10`

#### Start Command:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Environment Variables:
In Railway dashboard → Variables:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 2.3 Deploy
- Railway will auto-detect the `Procfile` and `requirements.txt`
- Click "Deploy"
- Wait for deployment to complete
- Copy your backend URL (e.g., `https://api-xyz.railway.app`)

---

## Step 3: Deploy Frontend on Railway

### 3.1 Add Frontend Service

1. In the same Railway project, click "Add Service"
2. Select "GitHub" → Deploy from same repository

### 3.2 Configure Frontend Service

#### Build Settings:
- **Base Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm run preview` (or use Node adapter)

#### Environment Variables:
In Railway dashboard → Frontend Service → Variables:
```
VITE_API_URL=https://api-xyz.railway.app
```
(Replace with your actual backend URL from Step 2.3)

### 3.3 Expose Frontend to Public
1. In Railway → Frontend Service → Settings
2. Generate a public URL
3. This is your public dashboard URL

---

## Step 4: Configure Environment Variables

### Backend (.env file):
Create `backend/.env.production`:
```
GROQ_API_KEY=your_groq_api_key
```

**OR** Set directly in Railway dashboard:
- Backend Service → Variables
- Add `GROQ_API_KEY=your_key`

### Frontend (.env file):
Create `frontend/.env.production`:
```
VITE_API_URL=https://your-railway-backend-url.railway.app
```

---

## Step 5: Verify Deployment

### Check Backend Health:
```bash
curl https://your-backend-url.railway.app/health
```

Response should be:
```json
{"status":"ok","service":"AI Policy Analyzer","rag_ready":true}
```

### Access Frontend:
Open your Railway frontend URL in browser:
```
https://your-frontend-url.railway.app
```

---

## Troubleshooting

### Issue: Backend returns 401 (Invalid API Key)
**Solution**: 
- Verify GROQ_API_KEY is set in Railway Variables
- Check the key is valid at https://console.groq.com/
- Redeploy after updating the variable

### Issue: Frontend shows connection errors
**Solution**:
- Verify VITE_API_URL is correctly set in frontend variables
- Check it matches your backend URL
- Clear browser cache and reload

### Issue: Slow startup/timeout
**Solution**:
- Sentence Transformers model takes ~30s to load
- Set a longer timeout in Railway if needed
- This is normal on first request

### Issue: FAISS index not found
**Solution**:
- PDFs must be in `backend/data/pdfs/`
- FAISS index is built on first startup
- If custom PDFs needed, add them before deployment

---

## Production Checklist

- [ ] GROQ_API_KEY is set securely in Railway
- [ ] Backend API URL is configured in frontend
- [ ] Health endpoint responds with `rag_ready: true`
- [ ] Frontend can reach backend without CORS errors
- [ ] Chat and Policy Evaluator both work
- [ ] Web search is functioning
- [ ] Sources are being retrieved correctly

---

## Custom Domain (Optional)

To use a custom domain:
1. In Railway → Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update frontend `VITE_API_URL` if needed

---

## Scaling Notes

- **Cold starts**: Railway keeps free projects warm, but paid plans have guaranteed uptime
- **Concurrent users**: Current setup handles moderate traffic
- **Data persistence**: FAISS index is rebuilt on startup (not persisted)
- **Memory**: Backend needs ~2GB RAM (include in Railway plan)

---

## Cost Estimation

**Railway Pricing** (as of 2026):
- Free tier: $5/month free credits
- Pay-as-you-go after: ~$0.09/hour per service
- 2 services (backend + frontend): ~$10-20/month for moderate use

---

## Support

For Railway-specific issues:
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

For application issues:
- Check backend logs in Railway dashboard
- Check frontend browser console (F12)
- Verify API configuration

---

## Next Steps

After successful deployment:
1. ✅ Test all features thoroughly
2. ✅ Share your production URL
3. ✅ Monitor logs for errors
4. ✅ Collect user feedback
5. ✅ Iterate on improvements

Happy deploying! 🚀
