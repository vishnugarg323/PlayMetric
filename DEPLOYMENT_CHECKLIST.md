# 🚀 Railway Deployment Checklist

## ✅ Pre-Deployment Completed

- [x] Consolidated all documentation into single README.md
- [x] Removed unnecessary files (docker-compose.railway.yml, populate_test_data.py, start-paime.ps1)
- [x] Cleaned and repopulated Railway MongoDB with fresh data
  - 10 users with realistic archetypes
  - 48,977 events across 7 collection types
  - $1,643.93 in revenue
- [x] Pushed clean code to GitHub (commit: bf898c5)

## 📋 Next Steps: Railway Deployment

### 1. Deploy Java Backend

**Railway Dashboard Steps:**
1. Go to https://railway.app/new
2. Click "+ New Service"
3. Select "GitHub Repo" → `vishnugarg323/PlayMetric`
4. **IMPORTANT**: In Settings → Service Settings:
   - **Service Name**: `playmetric-java-api`
   - **Root Directory**: `backend-java` ⚠️ **MUST SET THIS!**
   - **Builder**: Dockerfile (auto-detected)
5. Go to Variables tab and add Environment Variable:
   ```
   SPRING_DATA_MONGODB_URI=mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458/playmetric?authSource=admin
   ```
6. Click Deploy

**Expected Result**: 
- URL: `https://playmetric-java-api.up.railway.app`
- Swagger: `https://playmetric-java-api.up.railway.app/swagger-ui.html`

---

### 2. Deploy Python AI Service

**Railway Dashboard Steps:**
1. Click "+ New Service" (same project)
2. Select same GitHub repo
3. **IMPORTANT**: In Settings → Service Settings:
   - **Service Name**: `paime-analytics`
   - **Root Directory**: `backend-python` ⚠️ **MUST SET THIS!**
   - **Builder**: Dockerfile (auto-detected)
4. Go to Variables tab and add Environment Variables:
   ```
   MONGODB_URI=mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458
   DATABASE_NAME=playmetric
   ```
5. Click Deploy

**Expected Result**:
- URL: `https://paime-analytics.up.railway.app`
- Swagger: `https://paime-analytics.up.railway.app/docs`

---

### 3. Deploy Dashboard

**Railway Dashboard Steps:**
1. Click "+ New Service" (same project)
2. Select same GitHub repo
3. **IMPORTANT**: In Settings → Service Settings:
   - **Service Name**: `paime-dashboard`
   - **Root Directory**: `backend-python` ⚠️ **MUST SET THIS!**
   - **Dockerfile Path**: `Dockerfile.dashboard` ⚠️ **MUST SET THIS!**
   - **Builder**: Dockerfile (auto-detected)
4. Go to Variables tab and add Environment Variables:
   ```
   MONGODB_URI=mongodb://mongo:JpAlzHmXLTmvTMPEDNVqWwFbVzCEbFJC@gondola.proxy.rlwy.net:21458
   DATABASE_NAME=playmetric
   API_URL=https://paime-analytics.up.railway.app
   ```
5. Click Deploy

**Expected Result**:
- URL: `https://paime-dashboard.up.railway.app`

---

## 🧪 Post-Deployment Testing

### Test Java API
```bash
# Health check
curl https://playmetric-java-api.up.railway.app/actuator/health

# Test event ingestion
curl -X POST https://playmetric-java-api.up.railway.app/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "globalParams": {
      "userId": "test_user_001",
      "deviceId": "device123",
      "platform": "ANDROID",
      "sessionId": "session456",
      "timestamp": "2025-10-14T12:00:00Z"
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

# Get statistics
curl https://paime-analytics.up.railway.app/analytics/stats

# Get analytics overview
curl https://paime-analytics.up.railway.app/analytics/overview

# Get churn predictions
curl https://paime-analytics.up.railway.app/analytics/churn?limit=5
```

### Test Dashboard
- Visit: `https://paime-dashboard.up.railway.app`
- Verify all 6 metric cards display data
- Check all 8 charts render correctly
- Wait 30 seconds to test auto-refresh

---

## 📊 Current Database Stats

```
Collection Statistics:
- users: 10
- level_events: 24,639
- game_events: 328
- economy_events: 12,227
- mission_events: 4,824
- ads_events: 3,875
- ui_interaction_events: 3,412

Total events: 48,977

Revenue Statistics:
- Total Revenue: $1,643.93
- Paying Users: 10/10
- ARPPU: $164.39

User Archetypes:
- at_risk: 4 users
- casual: 2 users
- engaged: 1 user
- whale: 3 users
```

---

## 🎯 Final URLs

| Service | URL |
|---------|-----|
| **Java API** | https://playmetric-java-api.up.railway.app |
| **Java Swagger** | https://playmetric-java-api.up.railway.app/swagger-ui.html |
| **Python API** | https://paime-analytics.up.railway.app |
| **Python Swagger** | https://paime-analytics.up.railway.app/docs |
| **Dashboard** | https://paime-dashboard.up.railway.app |
| **GitHub Repo** | https://github.com/vishnugarg323/PlayMetric |

---

## ⚠️ Important Notes

1. **Railway Limits**: Free tier has 500 hours/month ($5 credit)
2. **MongoDB**: Already hosted on Railway (gondola.proxy.rlwy.net:21458)
3. **No docker-compose**: Railway uses individual Dockerfiles
4. **One Port Per Service**: Each service exposes only one public port
5. **Environment Variables**: Must be set in Railway Dashboard for each service

---

## 🐛 Troubleshooting

### ❌ Error: "Dockerfile does not exist"
**Cause**: Railway is looking in the wrong directory (root instead of subdirectory)

**Solution**:
1. Go to your service in Railway Dashboard
2. Click **Settings** tab
3. Scroll to **Service Settings**
4. Set **Root Directory**:
   - For Java: `backend-java`
   - For Python: `backend-python`
   - For Dashboard: `backend-python`
5. For Dashboard ONLY, also set **Dockerfile Path**: `Dockerfile.dashboard`
6. Click **Save** and redeploy

### Service won't deploy
- Check Dockerfile path is correct
- Verify Root Directory matches service location
- Ensure environment variables are set

### Dashboard shows 0 data
- Verify API_URL environment variable is correct
- Check Python API is running (test /health endpoint)
- Verify MongoDB connection works

### API returns 500 errors
- Check Railway logs in dashboard
- Verify MongoDB URI is correct
- Test MongoDB connection from Railway service

---

## ✅ Success Criteria

- [ ] All 3 services deployed successfully
- [ ] Java Swagger UI loads and shows API endpoints
- [ ] Python Swagger UI loads and shows 8 endpoints
- [ ] Dashboard displays all 6 metrics correctly
- [ ] Dashboard shows all 8 charts with data
- [ ] Can send test event via Java API
- [ ] Can fetch analytics via Python API
- [ ] Auto-refresh works on dashboard (30s interval)

---

**Ready to deploy! 🚀**
