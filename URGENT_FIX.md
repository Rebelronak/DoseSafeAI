# ⚠️ URGENT FIX - Backend Not Deployed

## Current Issue:
- ✅ Frontend is deployed on Vercel
- ❌ Backend is NOT deployed anywhere
- ❌ Frontend trying to connect to: `https://dosesafe-ai-backend.onrender.com` (doesn't exist yet)

## Solution: Deploy Backend NOW

### STEP 1: Deploy Backend to Render

1. **Go to Render Dashboard:**
   👉 https://dashboard.render.com

2. **Create New Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Connect GitHub: `Rebelronak/DoseSafeAI`
   - Click "Connect"

3. **Configure:**
   - **Name:** `dosesafe-ai-backend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** `Python 3`
   
   - **Build Command:**
   ```bash
   pip install --upgrade pip && pip install -r backend/requirements.txt && python -m spacy download en_core_web_sm
   ```
   
   - **Start Command:**
   ```bash
   cd backend && gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
   ```

4. **Environment Variables:**
   Click "Add Environment Variable":
   - `GROQ_API_KEY` = (get from https://console.groq.com/keys)
   - `PYTHON_VERSION` = `3.11.0`
   - `FLASK_ENV` = `production`

5. **Select Plan:**
   - Free ($0/month)

6. **Click "Create Web Service"**

7. **Wait 5-10 minutes** for deployment

8. **Copy the URL** (e.g., `https://dosesafe-ai-backend.onrender.com`)

### STEP 2: Update Frontend Environment Variable

**In Vercel Dashboard:**

1. Go to your project settings
2. Click "Environment Variables"
3. Find or add `VITE_API_URL`
4. Set value to: `https://your-actual-render-url.onrender.com`
5. Click "Save"
6. Redeploy frontend (Vercel → Deployments → Click "..." → Redeploy)

### STEP 3: Update CORS in Backend

After both are deployed, update `backend/app.py` with your actual Vercel URL:

```python
"origins": [
    "http://localhost:5173",
    "https://your-actual-vercel-url.vercel.app",  # UPDATE THIS
    "https://*.vercel.app"
]
```

Then push to GitHub (Render will auto-redeploy).

---

## Alternative: Quick Fix with Vercel Serverless Functions

If you want everything on Vercel, we need to create serverless API routes.

Would you like me to:
1. Help you deploy backend to Render (recommended)
2. Convert backend to Vercel serverless functions (complex)
3. Both

Let me know and I'll guide you through it!
