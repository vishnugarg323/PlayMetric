# 🚂 Railway Deployment - Quick Fix Guide

## ❌ Error: "Dockerfile does not exist"

This error occurs because Railway is looking for the Dockerfile in the **root directory** (`/`), but your Dockerfiles are in subdirectories (`/backend-java/` and `/backend-python/`).

---

## ✅ Solution: Set Root Directory for Each Service

### Step-by-Step Fix

#### 1️⃣ For Java Backend Service

After creating the service from GitHub:

1. Click on the service name in Railway Dashboard
2. Go to **Settings** tab (⚙️ icon)
3. Scroll down to **Service Settings** section
4. Find **Root Directory** field
5. Enter: `backend-java`
6. Click **Deploy** or wait for auto-redeploy

**What this does**: Tells Railway to look for Dockerfile at `backend-java/Dockerfile` instead of `Dockerfile`

---

#### 2️⃣ For Python API Service

1. Click on the Python service in Railway Dashboard
2. Go to **Settings** tab
3. Under **Service Settings**:
   - **Root Directory**: `backend-python`
4. Save and redeploy

**What this does**: Tells Railway to look at `backend-python/Dockerfile`

---

#### 3️⃣ For Dashboard Service

This one needs TWO settings:

1. Click on the Dashboard service
2. Go to **Settings** tab
3. Under **Service Settings**:
   - **Root Directory**: `backend-python`
   - **Dockerfile Path**: `Dockerfile.dashboard`
4. Save and redeploy

**Why both?**: 
- Root Directory tells Railway where to look (`backend-python/`)
- Dockerfile Path tells it which file to use (`Dockerfile.dashboard` instead of default `Dockerfile`)

---

## 🎯 Quick Verification Checklist

Before deploying each service, verify these settings:

### Java Backend
- ✅ Root Directory: `backend-java`
- ✅ Dockerfile Path: (leave empty, will use default `Dockerfile`)
- ✅ Builder: Dockerfile

### Python API
- ✅ Root Directory: `backend-python`
- ✅ Dockerfile Path: (leave empty, will use default `Dockerfile`)
- ✅ Builder: Dockerfile

### Dashboard
- ✅ Root Directory: `backend-python`
- ✅ Dockerfile Path: `Dockerfile.dashboard`
- ✅ Builder: Dockerfile

---

## 📸 Where to Find These Settings

```
Railway Dashboard
├── Your Project
│   ├── Service (e.g., playmetric-java-api)
│   │   ├── Deployments tab
│   │   ├── Variables tab
│   │   └── Settings tab ⬅️ YOU NEED THIS
│   │       ├── General
│   │       ├── Service Settings ⬅️ SET ROOT DIRECTORY HERE
│   │       │   ├── Service Name
│   │       │   ├── Root Directory ⬅️ ⬅️ ⬅️
│   │       │   ├── Dockerfile Path (optional)
│   │       │   └── Builder
│   │       ├── Networking
│   │       └── Danger Zone
```

---

## 🔄 Alternative: Create Railway.toml Files (NOT RECOMMENDED)

You could create separate `railway.toml` files in each subdirectory, but this is more complex. The Root Directory approach is simpler and recommended.

---

## ⚡ Quick Deploy Command (Alternative)

If you prefer using Railway CLI:

```bash
# Deploy Java Backend
cd backend-java
railway up

# Deploy Python API
cd ../backend-python
railway up

# Deploy Dashboard (with specific Dockerfile)
railway up --dockerfile Dockerfile.dashboard
```

But using the Dashboard with Root Directory is easier for managing multiple services.

---

## ✅ After Setting Root Directory

Your deployment should succeed! Check the logs to confirm:

```
✓ Building Dockerfile
✓ Docker build completed
✓ Deploying...
✓ Deployment successful
```

---

## 🆘 Still Having Issues?

### Check these:
1. Dockerfile actually exists in the specified directory
2. Root Directory path is correct (case-sensitive on some systems)
3. No typos in the directory name
4. GitHub repo is properly connected

### Verify locally:
```powershell
# From PlayMetric root directory
ls backend-java/Dockerfile      # Should exist
ls backend-python/Dockerfile    # Should exist
ls backend-python/Dockerfile.dashboard  # Should exist
```

---

**This should fix your deployment error! 🚀**
