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

See `phase7_frontend_experience/README.md` for Vercel deployment steps.

### Quick Steps
1. Go to https://vercel.com
2. Import your GitHub repository
3. Configure:
   - **Framework**: Next.js
   - **Root Directory**: `phase7_frontend_experience`
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL`: `https://<your-render-service>.onrender.com`
5. Deploy!
