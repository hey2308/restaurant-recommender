# Deployment Guide

## Phase 9: Backend Deployment on Render

### Prerequisites
1. GitHub repository pushed with all code
2. Render account (free tier available at https://render.com)
3. Groq API key

### Deployment Steps

#### Option 1: Using render.yaml (Blueprints)
1. Go to Render Dashboard → Blueprints
2. Connect your GitHub repository
3. Render will automatically detect `render.yaml` and create the service
4. Add environment variable `GROQ_API_KEY` in the dashboard
5. Deploy!

#### Option 2: Manual Web Service Creation
1. Go to Render Dashboard → New → Web Service
2. Connect your GitHub repository
3. Configure:
   - **Name**: `bitewise-backend` (or your preferred name)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r phase6_backend_api/requirements.txt`
   - **Start Command**: `cd phase6_backend_api && gunicorn app:app --bind 0.0.0.0:$PORT`
4. Add environment variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `DATA_ROOT`: `/opt/render/project/src` (Render default)
5. Create Web Service

### Verify Deployment
Once deployed, check:
```
https://<your-service>.onrender.com/api/v1/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Phase 10: Frontend Deployment on Vercel

### Prerequisites
1. GitHub repository with pushed code
2. Vercel account (free at https://vercel.com)
3. Backend deployed on Render (Phase 9 complete) with working URL

### Deployment Steps

#### Option 1: Vercel Dashboard (Recommended)
1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Import your GitHub repository: `hey2308/restaurant-recommender`
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `phase7_frontend_experience` (⚠️ Important!)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Add Environment Variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Render backend URL (e.g., `https://bitewise-backend.onrender.com`)
6. Click "Deploy"

#### Option 2: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd phase7_frontend_experience
vercel --prod
```

### Verify Deployment
Visit your deployed URL:
```
https://<your-project>.vercel.app
```

### Post-Deployment
- Vercel auto-deploys on every push to main
- Update `NEXT_PUBLIC_API_URL` if backend URL changes
- Add custom domain in Vercel Settings → Domains (optional)

---

## Production Checklist

- [ ] Backend deployed on Render with `GROQ_API_KEY` set
- [ ] Frontend deployed on Vercel with `NEXT_PUBLIC_API_URL` set
- [ ] CORS enabled on backend (already configured)
- [ ] Test end-to-end recommendation flow
- [ ] Verify LLM explanations are showing (not fallback)
- [ ] Custom domains configured (optional)
