# 🚀 Quick Deployment Guide for DoseSafe AI

## ✅ Files Created for Deployment

I've prepared your project for deployment with the following configurations:

### 📁 Configuration Files Created:

1. **`render.yaml`** - Backend deployment configuration for Render
2. **`vercel.json`** - Frontend deployment configuration for Vercel
3. **`frontend/.env.production`** - Production environment variables
4. **`frontend/.env.development`** - Development environment variables
5. **`frontend/src/config/api.js`** - API endpoint configuration
6. **Updated `backend/requirements.txt`** - Fixed PyTorch version for deployment
7. **Updated `backend/app.py`** - Added production CORS and server configuration

---

## 🎯 Step-by-Step Deployment

### **STEP 1: Commit and Push to GitHub**

```bash
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

### **STEP 2: Deploy Backend to Render**

1. Go to **https://render.com** and sign in with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect repository: **`Rebelronak/DoseSafeAI`**
4. Render will auto-detect `render.yaml` configuration
5. Add environment variable:
   - **Key:** `GROQ_API_KEY`
   - **Value:** Your Groq API key from https://console.groq.com
6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment
8. **Copy your backend URL:** `https://dosesafe-ai-backend.onrender.com`

### **STEP 3: Update Frontend Configuration**

Edit **`frontend/.env.production`** with your actual Render URL:
```bash
VITE_API_URL=https://dosesafe-ai-backend.onrender.com
```
Replace with YOUR actual URL from Render.

### **STEP 4: Deploy Frontend to Vercel**

**Option A - Vercel CLI:**
```bash
npm install -g vercel
vercel login
cd frontend
vercel --prod
```

**Option B - Vercel Dashboard:**
1. Go to **https://vercel.com** and sign in with GitHub
2. Click **"Add New..."** → **"Project"**
3. Import **`Rebelronak/DoseSafeAI`**
4. Configure:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add Environment Variable:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://dosesafe-ai-backend.onrender.com` (your actual backend URL)
6. Click **"Deploy"**

### **STEP 5: Update CORS (IMPORTANT!)**

After getting your Vercel URL, update **`backend/app.py`**:

```python
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "https://your-actual-vercel-url.vercel.app",  # UPDATE THIS
            "https://*.vercel.app"
        ]
    }
})
```

Then push the update:
```bash
git add backend/app.py
git commit -m "Update CORS for production"
git push origin main
```

Render will automatically redeploy.

---

## 🌐 Access Your Deployed App

| Service | URL | Platform |
|---------|-----|----------|
| **Frontend** | https://dosesafe-ai.vercel.app | Vercel |
| **Backend** | https://dosesafe-ai-backend.onrender.com | Render |
| **Health Check** | https://dosesafe-ai-backend.onrender.com/health | Render |

---

## ✅ Verification Checklist

After deployment:

- [ ] Visit backend `/health` endpoint - should return `{"status": "healthy"}`
- [ ] Visit frontend URL - should load the homepage
- [ ] Test prescription upload - should work end-to-end
- [ ] Check browser console - no CORS errors
- [ ] Test AI chatbot - should get responses (if API key configured)
- [ ] Test scan history - should save and load

---

## ⚠️ Important Notes

### Render Free Tier:
- Backend sleeps after 15 minutes of inactivity
- First request after sleep: 30-50 second delay
- Keep warm with UptimeRobot (optional)

### Vercel Free Tier:
- Unlimited deployments
- Automatic HTTPS
- Global CDN

### Environment Variables:
- Never commit `.env` files to GitHub
- Set `GROQ_API_KEY` in Render dashboard
- Set `VITE_API_URL` in Vercel dashboard

---

## 🐛 Troubleshooting

### Backend Won't Deploy
- Check Render build logs
- Verify `requirements.txt` has no typos
- Ensure Python 3.11.0 is selected

### Frontend Can't Connect to Backend
- Check `VITE_API_URL` in Vercel environment variables
- Verify CORS origins in `backend/app.py`
- Check browser console for errors

### CORS Errors
- Update `backend/app.py` with exact Vercel URL
- Redeploy backend after CORS changes
- Clear browser cache

---

## 📊 Monitoring

### Render Dashboard:
- View logs: https://dashboard.render.com
- Monitor CPU/Memory usage
- Check deployment status

### Vercel Dashboard:
- View analytics: https://vercel.com/dashboard
- Check function logs
- Monitor performance

---

## 🎉 Success!

Your DoseSafe AI is now live and accessible worldwide! 

**Next Steps:**
- Share your app with users
- Monitor performance
- Add custom domain (optional)
- Set up monitoring alerts

---

## 📞 Need Help?

If you encounter issues:
1. Check Render and Vercel logs
2. Verify all environment variables are set
3. Test API endpoints with Postman/curl
4. Review CORS configuration

**Your project is ready for production! 🚀**
