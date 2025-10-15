# 🚂 Railway Deployment Guide - Two Separate Services

## 📋 Overview

You're deploying **2 separate services** on Railway from the same GitHub repo:
1. **Java Backend** (from `backend-java/`)
2. **Python AI Service** (from `backend-python/`)

---

## ✅ Pre-Deployment Setup (DONE)

I've created `railway.toml` files in each subdirectory:
- `backend-java/railway.toml` - Tells Railway how to build Java service
- `backend-python/railway.toml` - Tells Railway how to build Python service

---

## 🚀 Deployment Steps

### Method 1: Using Railway Dashboard (RECOMMENDED)

#### Step 1: Deploy Java Backend

1. Go to https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Select **`vishnugarg323/PlayMetric`**
4. Railway will detect the repo - click **"Add variables"** (skip for now)
5. After service is created, click on it
6. Go to **Settings** tab
7. Under **Build** section:
   - **Root Directory**: `backend-java`
   - **Builder**: Dockerfile (auto-detected)
8. Go to **Variables** tab and add:
   ```
   SPRING_DATA_MONGODB_URI=mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458/playmetric?authSource=admin
   ```
9. Click **Deploy** (or it auto-deploys)
10. Rename service to `playmetric-java-api` (Settings → General → Service Name)

**Expected Result**: Service builds and deploys successfully
**Test URL**: `https://playmetric-java-api.up.railway.app/swagger-ui.html`

---

#### Step 2: Deploy Python AI Service

1. In the same Railway dashboard, click **"+ New"** → **"GitHub Repo"**
2. Or create a **new project**: https://railway.app/new
3. Select the **same repo**: `vishnugarg323/PlayMetric`
4. After service is created, click on it
5. Go to **Settings** tab
6. Under **Build** section:
   - **Root Directory**: `backend-python`
   - **Builder**: Dockerfile (auto-detected)
7. Go to **Variables** tab and add:
   ```
   MONGODB_URI=mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458
   DATABASE_NAME=playmetric
   PORT=8000
   ```
8. Click **Deploy**
9. Rename service to `paime-analytics`

**Expected Result**: Service builds and deploys successfully
**Test URL**: `https://paime-analytics.up.railway.app/docs`

---

### Method 2: Using Railway CLI

If you prefer command line:

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy Java Backend
cd backend-java
railway init
# Select: Create new project → Enter project name: playmetric-java-api
railway up
railway variables set SPRING_DATA_MONGODB_URI="mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458/playmetric?authSource=admin"

# Deploy Python AI Service
cd ../backend-python
railway init
# Select: Create new project → Enter project name: paime-analytics
railway up
railway variables set MONGODB_URI="mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458"
railway variables set DATABASE_NAME="playmetric"
railway variables set PORT="8000"
```

---

## 🎯 Critical Settings for Each Service

### Java Backend Settings
- **Service Name**: `playmetric-java-api`
- **Root Directory**: `backend-java`
- **Port**: 8080 (auto-detected from Dockerfile)
- **Environment Variables**:
  ```
  SPRING_DATA_MONGODB_URI=mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458/playmetric?authSource=admin
  ```

### Python AI Settings
- **Service Name**: `paime-analytics`
- **Root Directory**: `backend-python`
- **Port**: 8000 (auto-detected from Dockerfile)
- **Environment Variables**:
  ```
  MONGODB_URI=mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458
  DATABASE_NAME=playmetric
  PORT=8000
  ```

---

## 🧪 Testing After Deployment

### Test Java API
```bash
# Health check
curl https://playmetric-java-api.up.railway.app/actuator/health

# Swagger UI (open in browser)
https://playmetric-java-api.up.railway.app/swagger-ui.html

# Test event ingestion
curl -X POST https://playmetric-java-api.up.railway.app/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "globalParams": {
      "userId": "test_user_001",
      "deviceId": "device123",
      "platform": "ANDROID",
      "sessionId": "session456",
      "timestamp": "2025-10-15T12:00:00Z"
    },
    "eventType": "LEVEL_COMPLETE",
    "levelId": 1,
    "score": 1500,
    "stars": 3,
    "completed": true,
    "timeTaken": 120
  }'
```

### Test Python API
```bash
# Health check
curl https://paime-analytics.up.railway.app/health

# Swagger UI (open in browser)
https://paime-analytics.up.railway.app/docs

# Get statistics
curl https://paime-analytics.up.railway.app/analytics/stats

# Get overview
curl https://paime-analytics.up.railway.app/analytics/overview
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Dockerfile does not exist"
**Solution**: Make sure **Root Directory** is set correctly in Railway Settings
- Java: `backend-java`
- Python: `backend-python`

### Issue 2: "Build failed - No Dockerfile found"
**Solution**: The `railway.toml` files should fix this. If not, check:
1. Files are committed to GitHub
2. Root Directory path is correct (case-sensitive)
3. Dockerfile exists in the subdirectory

### Issue 3: "Port already in use" or "Service not responding"
**Solution**: Railway auto-detects the port from EXPOSE in Dockerfile. Make sure:
- Java Dockerfile has `EXPOSE 8080`
- Python Dockerfile has `EXPOSE 8000`

### Issue 4: "Cannot connect to MongoDB"
**Solution**: Check environment variables are set correctly with exact connection string

---

## 📊 Final URLs

After successful deployment:

| Service | URL | Description |
|---------|-----|-------------|
| Java API | `https://playmetric-java-api.up.railway.app` | Event ingestion |
| Java Swagger | `https://playmetric-java-api.up.railway.app/swagger-ui.html` | API docs |
| Python API | `https://paime-analytics.up.railway.app` | Analytics API |
| Python Swagger | `https://paime-analytics.up.railway.app/docs` | API docs |
| Python Dashboard | `https://paime-analytics.up.railway.app:8050` | Dashboard (if exposed) |

**Note**: Railway only exposes ONE port per service publicly. The dashboard on port 8050 won't be accessible unless you deploy it as a separate service.

---

## 📦 What's Different from Before

**Before**: All code was in root directory
- Railway could find `Dockerfile` directly at `/Dockerfile`

**Now**: Code is in subdirectories
- Railway needs to look in `/backend-java/Dockerfile` or `/backend-python/Dockerfile`
- Must set **Root Directory** in Railway Settings to tell it where to look

---

## ✅ Success Checklist

- [ ] Created service for Java backend
- [ ] Set Root Directory: `backend-java`
- [ ] Added MongoDB environment variable
- [ ] Java service deployed successfully
- [ ] Java Swagger UI loads
- [ ] Created service for Python API
- [ ] Set Root Directory: `backend-python`
- [ ] Added MongoDB + DATABASE_NAME variables
- [ ] Python service deployed successfully
- [ ] Python Swagger UI loads
- [ ] Can fetch analytics data

---

**Your services should now deploy successfully! 🚀**

If you still face issues, share the error message and I'll help you debug.
