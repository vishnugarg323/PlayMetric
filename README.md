# 🎮 PAIME - PlayMetric AI Metrics Engine

> AI-Powered Game Analytics Platform with Real-time Insights

[![Java](https://img.shields.io/badge/Java-21-orange.svg)](https://openjdk.java.net/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 Overview

PAIME is a comprehensive game analytics platform that combines real-time data collection, AI-powered analysis, and beautiful visualizations to help game developers understand their players and improve their games.

### Features

- **📊 Real-time Analytics**: Track DAU, MAU, retention, revenue, and more
- **🤖 AI Predictions**: Churn risk prediction using machine learning
- **🎮 Level Analysis**: Identify difficult levels and drop-off points
- **💡 Smart Recommendations**: AI-powered suggestions to improve your game
- **👥 User Segmentation**: Categorize players (whales, engaged, casual, at-risk)
- **📈 Beautiful Dashboard**: Interactive Plotly Dash dashboard with auto-refresh

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for data population)
- Git

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/vishnugarg323/PlayMetric.git
cd PlayMetric

# 2. Start Docker Desktop (if not running)

# 3. Start all services
docker-compose up -d --build

# 4. Wait for services to be healthy (30 seconds)

# 5. Populate test data
python populate_comprehensive_data.py

# 6. Access services
```

**Service URLs:**
- **Dashboard**: http://localhost:8050
- **Java Swagger**: http://localhost:8080/swagger-ui.html
- **Python Swagger**: http://localhost:8000/docs

### Verify Services

```bash
# Check Java API (Swagger UI)
curl http://localhost:8080/swagger-ui.html

# Check Python API
curl http://localhost:8000/health

# Check Dashboard
curl http://localhost:8050

# Check data statistics
curl http://localhost:8000/analytics/stats
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              PAIME System                        │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────┐     ┌──────────────┐             │
│  │ MongoDB  │◄────│ Java Backend │             │
│  │ Railway  │     │ Spring Boot  │             │
│  │          │     │ Port: 8080   │             │
│  └────┬─────┘     └──────────────┘             │
│       │                                          │
│       │           ┌──────────────┐              │
│       └──────────►│  Python AI   │              │
│                   │ FastAPI:8000 │              │
│                   │ Dash:8050    │              │
│                   └──────┬───────┘              │
│                          │                       │
│                   ┌──────▼──────┐               │
│                   │  ML Models  │               │
│                   │  Analytics  │               │
│                   └─────────────┘               │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Components

1. **Java Backend** - Event ingestion API (Spring Boot)
2. **Python AI Service** - Analytics API (FastAPI)
3. **Dashboard** - Real-time visualization (Plotly Dash)
4. **MongoDB** - Data storage (Railway hosted)

---

## 📚 API Documentation

### Java Backend (Event Ingestion)

**Base URL**: `http://localhost:8080`

#### POST /api/events
Unified endpoint for all event types.

```json
{
  "globalParams": {
    "userId": "user123",
    "deviceId": "device456",
    "platform": "ANDROID",
    "sessionId": "session789",
    "timestamp": "2025-10-15T12:00:00Z"
  },
  "eventType": "LEVEL_COMPLETE",
  "levelId": 1,
  "score": 1500,
  "stars": 3,
  "completed": true,
  "timeTaken": 120
}
```

### Python AI Service (Analytics)

**Base URL**: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/analytics/overview` | GET | Complete metrics overview |
| `/analytics/churn` | GET | Churn predictions |
| `/analytics/levels` | GET | Level difficulty analysis |
| `/analytics/users/segments` | GET | User segmentation |
| `/analytics/users/{id}` | GET | Individual user analysis |
| `/analytics/recommendations` | GET | AI recommendations |
| `/analytics/stats` | GET | Raw statistics |

---

## 📊 Dashboard

### Access

- **Local**: http://localhost:8050

### Features

**6 Metric Cards**:
- Total Users
- Daily Active Users (DAU)
- Average Session Duration
- Total Revenue
- Day 1 Retention
- Total Events

**8 Interactive Charts**:
- User Activity Trends (DAU/WAU/MAU)
- Platform Distribution
- Level Difficulty Heatmap
- Level Progression Funnel
- Drop-off Levels
- Churn Risk Distribution
- High-Risk Users
- AI Recommendations

**Auto-refresh**: Every 30 seconds

---

## 🗄️ Data Population

### Generate Test Data

```bash
# Generate 10 users with 48K+ events
python populate_comprehensive_data.py
```

This creates:
- 10 user profiles with realistic archetypes
- 48,000+ events across 7 types
- Revenue transactions
- 30-day activity history

### User Archetypes

- **Whale** (5%): High spenders, 100-200 sessions
- **Engaged** (25%): Active players, 80-150 sessions
- **Casual** (40%): Regular players, 30-80 sessions
- **At-Risk** (20%): Declining activity, 10-30 sessions
- **Dormant** (10%): Inactive, 5-15 sessions

---

## 📁 Project Structure

```
PlayMetric/
├── backend-java/              # Java Spring Boot API
│   ├── src/main/
│   │   ├── java/org/playmetric/
│   │   └── resources/application.yml
│   ├── pom.xml
│   └── Dockerfile
│
├── backend-python/            # Python AI Service
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── unified_main.py   # Unified FastAPI + Dash
│   │   ├── database.py       # MongoDB connection
│   │   ├── models/           # ML models
│   │   ├── services/         # Analytics services
│   │   └── dashboard/        # Dash dashboard
│   ├── requirements.txt
│   ├── Dockerfile
│   └── Dockerfile.dashboard
│
├── docker-compose.yml         # Local development orchestration
├── populate_comprehensive_data.py  # Data generator
└── README.md                  # This file
```

---

## 🔧 Configuration

### Environment Variables

#### Java Backend
```bash
SPRING_DATA_MONGODB_URI=mongodb://user:pass@host:port/dbname?authSource=admin
SERVER_PORT=8080
```

#### Python AI Service
```bash
MONGODB_URI=mongodb://user:pass@host:port
DATABASE_NAME=playmetric
PORT=8000
```

---

## 🚂 Railway Deployment

### Deploy Using Railway CLI

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy Java Backend
cd backend-java
railway init  # Create new project
railway up    # Deploy
railway variables set SPRING_DATA_MONGODB_URI="<your-mongodb-uri>"

# 4. Deploy Python AI Service
cd ../backend-python
railway init  # Create new project
railway up    # Deploy
railway variables set MONGODB_URI="<your-mongodb-uri>"
railway variables set DATABASE_NAME="playmetric"
```

**Note**: Deploy from subdirectories using Railway CLI. Each service is a separate Railway project.

---

## 🧪 Testing

### Test Endpoints

```bash
# Java API health (Swagger UI)
curl http://localhost:8080/swagger-ui.html

# Python API health
curl http://localhost:8000/health

# Get analytics overview
curl http://localhost:8000/analytics/overview

# Get statistics
curl http://localhost:8000/analytics/stats
```

### Send Test Event

```bash
curl -X POST http://localhost:8080/api/events \
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

---

## 🐛 Troubleshooting

### Dashboard shows no data
**Solution**: Run `python populate_comprehensive_data.py`

### Services won't start
**Solution**: Check Docker is running and ports are available
```bash
docker ps
netstat -ano | findstr :8080
netstat -ano | findstr :8000
netstat -ano | findstr :8050
```

### MongoDB connection error
**Solution**: Verify MongoDB URI in docker-compose.yml or environment variables

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 👤 Author

**Vishnu Garg**
- GitHub: [@vishnugarg323](https://github.com/vishnugarg323)
- Repository: [PlayMetric](https://github.com/vishnugarg323/PlayMetric)

---

**Built with ❤️ for game developers who want to understand their players better.**

🎮 Happy Gaming! 🚀
