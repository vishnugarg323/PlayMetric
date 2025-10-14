# 🎮 PAIME - PlayMetric AI Metrics Engine# PlayMetric - Game Analytics Platform



> AI-Powered Game Analytics Platform with Real-time Insights[![Java](https://img.shields.io/badge/Java-21-orange.svg)](https://openjdk.java.net/)

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5.0-brightgreen.svg)](https://spring.io/projects/spring-boot)

[![Java](https://img.shields.io/badge/Java-21-orange.svg)](https://openjdk.java.net/)[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)](https://www.mongodb.com/)

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-brightgreen.svg)](https://spring.io/projects/spring-boot)

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)A comprehensive game analytics platform designed to track, analyze, and provide insights into game events for AI-driven analysis. Built with Spring Boot 3.5.0 and Java 21, optimized for Unity game integration and AI/ML analytics.

[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)

[![Railway](https://img.shields.io/badge/Deploy-Railway-purple.svg)](https://railway.app)## 🎯 Overview



---PlayMetric is a production-ready game analytics API that provides:



## 📋 Table of Contents- **Unified Event Tracking**: Single POST endpoint for all event types

- **Automatic User Management**: User profiles created and updated automatically

- [Overview](#overview)- **AI-Ready Data Structure**: Optimized for machine learning and data analysis

- [Architecture](#architecture)- **Comprehensive Event Types**: 100+ predefined event types covering all game scenarios

- [Features](#features)- **Rich Analytics Endpoints**: RESTful APIs for data retrieval and analysis

- [Quick Start](#quick-start)- **Full Documentation**: OpenAPI/Swagger documentation for all endpoints

- [Railway Deployment](#railway-deployment)

- [API Documentation](#api-documentation)## 🚀 Key Features

- [Dashboard](#dashboard)

- [Data Population](#data-population)### Event Tracking

- [Project Structure](#project-structure)- **Single POST Endpoint**: `/api/events` - One endpoint for all event types

- [Contributing](#contributing)- **Global Parameters**: Consistent user, device, and session tracking across all events

- **Automatic Routing**: Events automatically routed to appropriate collections

---- **Real-time Processing**: Instant event recording and user profile updates



## 🎯 Overview### Event Categories

1. **Session Events** - Game sessions, pause/resume tracking

PAIME is a comprehensive game analytics platform that combines real-time data collection, AI-powered analysis, and beautiful visualizations to help game developers understand their players and improve their games.2. **Level Events** - Level progression, completion, difficulty metrics

3. **Game Events** - Gameplay mechanics, scores, achievements

### What PAIME Does4. **Economy Events** - IAP, virtual currency, transactions

5. **Social Events** - Multiplayer, guilds, sharing

- **📊 Real-time Analytics**: Track DAU, MAU, retention, revenue, and more6. **Achievement Events** - Unlocks, progress, milestones

- **🤖 AI Predictions**: Churn risk prediction using machine learning7. **Ad Events** - Ad impressions, revenue, engagement

- **🎮 Level Analysis**: Identify difficult levels and drop-off points8. **UI Events** - User interface interactions, navigation

- **💡 Smart Recommendations**: AI-powered suggestions to improve your game9. **Performance Events** - Errors, crashes, performance metrics

- **👥 User Segmentation**: Categorize players (whales, engaged, casual, at-risk)

- **📈 Beautiful Dashboard**: Interactive Plotly Dash dashboard with auto-refresh### Analytics Capabilities

- User retention and churn analysis

---- Level difficulty calibration

- Monetization optimization

## 🏗️ Architecture- Session engagement metrics

- Cross-platform analytics

```- Cohort analysis

┌─────────────────────────────────────────────────────────────┐- Revenue tracking (IAP + Ads)

│                       PAIME System                           │

├─────────────────────────────────────────────────────────────┤## 📋 Requirements

│                                                              │

│  ┌──────────┐     ┌──────────────┐     ┌────────────────┐ │- **Java**: JDK 21 or higher

│  │ MongoDB  │◄────│ Java Backend │◄────│ Game Clients   │ │- **Maven**: 3.6+ (for building)

│  │ Railway  │     │ Spring Boot  │     │ (Mobile/Web)   │ │- **MongoDB**: 4.4+ (for data storage)

│  │          │     │ Port: 8080   │     │                │ │- **Memory**: Minimum 512MB RAM

│  └────┬─────┘     └──────────────┘     └────────────────┘ │

│       │                                                     │## 🛠️ Installation

│       │           ┌──────────────┐                         │

│       └──────────►│  Python AI   │                         │### 1. Clone the Repository

│                   │ FastAPI:8000 │                         │```bash

│                   │ Dash:8050    │                         │git clone https://github.com/vishnugarg323/PlayMetric.git

│                   └──────┬───────┘                         │cd PlayMetric

│                          │                                  │```

│                   ┌──────▼──────┐                          │

│                   │  ML Models  │                          │### 2. Configure MongoDB

│                   │  Analytics  │                          │Edit `src/main/resources/application.yml`:

│                   └─────────────┘                          │```yaml

│                                                              │spring:

└─────────────────────────────────────────────────────────────┘  data:

```    mongodb:

      uri: "mongodb://your-mongodb-host:27017/playmetric"

### Components```



1. **Java Backend** - Event ingestion API (Spring Boot)### 3. Build the Project

2. **Python AI Service** - Analytics API (FastAPI)```bash

3. **Dashboard** - Real-time visualization (Plotly Dash)mvn clean package

4. **MongoDB** - Data storage (Railway hosted)```



---### 4. Run the Application

```bash

## ✨ Featuresjava -jar target/playmetric-parent-1.0-SNAPSHOT.jar

```

### Analytics Dashboard

- 📊 6 Key metric cards (DAU, MAU, Revenue, Retention, etc.)The application will start on `http://localhost:8080`

- 📈 8 Interactive charts

- 🔄 Auto-refresh every 30 seconds## 📚 API Documentation

- 🌙 Dark theme

- 📱 Responsive design### Swagger UI

Access the interactive API documentation at:

### AI/ML Models```

- **Churn Predictor**: Random Forest classifier with 10 featureshttp://localhost:8080/swagger-ui.html

- **Level Analyzer**: Difficulty scoring algorithm (0-100)```

- **Analytics Engine**: Real-time aggregations

- **Recommendation Engine**: Priority-based insights### OpenAPI Spec

Download the OpenAPI specification at:

### Event Types Supported```

- Level events (start, complete, fail)http://localhost:8080/api-docs

- Game sessions (start, end)```

- Economy (purchases, earnings, spending)

- Missions (start, complete)## 🎮 Unity Integration

- Ads (impressions, rewards)

- UI interactions### Sending Events from Unity



---```csharp

using UnityEngine;

## 🚀 Quick Startusing UnityEngine.Networking;

using System.Collections;

### Prerequisitesusing System.Text;



- Docker & Docker Composepublic class PlayMetricClient : MonoBehaviour

- Python 3.11+ (for data population){

- Git    private const string API_URL = "http://your-server:8080/api/events";

    private string userId;

### Local Development    private string sessionId;



```bash    void Start()

# 1. Clone repository    {

git clone https://github.com/vishnugarg323/PlayMetric.git        userId = SystemInfo.deviceUniqueIdentifier;

cd PlayMetric        sessionId = System.Guid.NewGuid().ToString();

        

# 2. Start services        // Send session start event

docker-compose up -d        SendSessionStart();

    }

# 3. Populate test data

python populate_comprehensive_data.py    // Send a level complete event

    public void OnLevelComplete(string levelId, int score, int stars)

# 4. Access services    {

# Dashboard: http://localhost:8050        var eventData = new

# Java Swagger: http://localhost:8080/swagger-ui.html        {

# Python Swagger: http://localhost:8000/docs            globalParams = new

```            {

                userId = userId,

### Verify Services                deviceId = SystemInfo.deviceUniqueIdentifier,

                deviceModel = SystemInfo.deviceModel,

```bash                osVersion = SystemInfo.operatingSystem,

# Check Java API                platform = Application.platform.ToString(),

curl http://localhost:8080/actuator/health                appVersion = Application.version,

                sessionId = sessionId,

# Check Python API                sessionDuration = (long)(Time.realtimeSinceStartup * 1000)

curl http://localhost:8000/health            },

            eventType = "LEVEL_COMPLETE",

# Check data statistics            gameId = "my_awesome_game",

curl http://localhost:8000/analytics/stats            levelId = levelId,

```            completed = true,

            score = score,

---            starsEarned = stars,

            levelDuration = 120000

## 🚂 Railway Deployment        };



### Overview        StartCoroutine(SendEventCoroutine(eventData));

    }

Railway deployment uses **3 separate services**:

1. Java Backend (Swagger at `/swagger-ui.html`)    // Send economy purchase event

2. Python API (Swagger at `/docs`)    public void OnPurchase(string itemId, double price)

3. Dashboard (Standalone)    {

        var eventData = new

### Step-by-Step Deployment        {

            globalParams = GetGlobalParams(),

#### 1. Create Railway Project            eventType = "ECONOMY_IAP_PURCHASE",

            transactionId = System.Guid.NewGuid().ToString(),

```bash            itemId = itemId,

# Install Railway CLI (optional)            realMoneyValue = price,

npm install -g @railway/cli            currencyType = "USD"

        };

# Login

railway login        StartCoroutine(SendEventCoroutine(eventData));

    }

# Or use Railway Dashboard: https://railway.app/new

```    private object GetGlobalParams()

    {

#### 2. Deploy Java Backend        return new

        {

```            userId = userId,

In Railway Dashboard:            deviceId = SystemInfo.deviceUniqueIdentifier,

1. Click "+ New Service"            deviceModel = SystemInfo.deviceModel,

2. Select "GitHub Repo" → Your PlayMetric repo            osVersion = SystemInfo.operatingSystem,

3. Configure:            platform = Application.platform.ToString(),

   - Service Name: playmetric-java-api            appVersion = Application.version,

   - Root Directory: backend-java            sessionId = sessionId,

   - Environment Variables:            sessionDuration = (long)(Time.realtimeSinceStartup * 1000)

     SPRING_DATA_MONGODB_URI=<your-mongodb-uri>        };

4. Deploy    }

```

    private IEnumerator SendEventCoroutine(object eventData)

**Result**: `https://playmetric-java-api.up.railway.app`    {

        string jsonData = JsonUtility.ToJson(eventData);

#### 3. Deploy Python API        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);



```        using (UnityWebRequest request = new UnityWebRequest(API_URL, "POST"))

1. Click "+ New Service" (same repo)        {

2. Configure:            request.uploadHandler = new UploadHandlerRaw(bodyRaw);

   - Service Name: paime-analytics            request.downloadHandler = new DownloadHandlerBuffer();

   - Root Directory: backend-python            request.SetRequestHeader("Content-Type", "application/json");

   - Environment Variables:

     MONGODB_URI=<your-mongodb-uri>            yield return request.SendWebRequest();

     DATABASE_NAME=playmetric

3. Deploy            if (request.result == UnityWebRequest.Result.Success)

```            {

                Debug.Log("Event sent successfully!");

**Result**: `https://paime-analytics.up.railway.app`            }

            else

#### 4. Deploy Dashboard            {

                Debug.LogError($"Error sending event: {request.error}");

```            }

1. Click "+ New Service" (same repo)        }

2. Configure:    }

   - Service Name: paime-dashboard}

   - Root Directory: backend-python```

   - Dockerfile Path: Dockerfile.dashboard

   - Environment Variables:## 📊 API Endpoints

     MONGODB_URI=<your-mongodb-uri>

     DATABASE_NAME=playmetric### Event Recording

     API_URL=https://paime-analytics.up.railway.app

3. Deploy#### POST /api/events

```Record any type of game event.



**Result**: `https://paime-dashboard.up.railway.app`**Request Body:**

```json

### Railway URLs{

  "globalParams": {

| Service | URL | Description |    "userId": "user_12345",

|---------|-----|-------------|    "deviceId": "device_abc",

| Java API | `https://playmetric-java-api.up.railway.app` | Event ingestion |    "deviceModel": "iPhone 14 Pro",

| Java Swagger | `.../swagger-ui.html` | Java API docs |    "osVersion": "iOS 17.1",

| Python API | `https://paime-analytics.up.railway.app` | Analytics API |    "platform": "iOS",

| Python Swagger | `.../docs` | Python API docs |    "appVersion": "1.0.0",

| Dashboard | `https://paime-dashboard.up.railway.app` | Analytics dashboard |    "sessionId": "session_xyz",

    "sessionDuration": 1800000

### Important Notes  },

  "eventType": "LEVEL_COMPLETE",

- Railway does **NOT** use docker-compose files  "gameId": "adventure_mode",

- Each service needs its own `Dockerfile`  "levelId": "level_1_1",

- Only **ONE port** exposed publicly per service  "completed": true,

- MongoDB already hosted on Railway  "score": 1500,

  "starsEarned": 3

---}

```

## 📚 API Documentation

### Data Retrieval

### Java Backend (Event Ingestion)

#### GET /api/events

**Base URL**: `http://localhost:8080` or `https://playmetric-java-api.up.railway.app`Get all events grouped by type.



#### POST /api/events#### GET /api/events/users

Unified endpoint for all event types.Get all users with activity metrics.



```json#### GET /api/events/users/{userId}

{Get detailed information for a specific user.

  "globalParams": {

    "userId": "user123",#### GET /api/events/users/{userId}/events

    "deviceId": "device456",Get all events for a specific user across all types.

    "platform": "ANDROID",

    "sessionId": "session789",#### GET /api/events/game

    "timestamp": "2025-10-14T10:30:00Z"Get all game session events.

  },

  "eventType": "LEVEL_COMPLETE",#### GET /api/events/level

  "levelId": 1,Get all level progression events.

  "score": 1500,

  "stars": 3,#### GET /api/events/level/{levelId}

  "completed": true,Get all events for a specific level.

  "timeTaken": 120

}#### GET /api/events/game/{gameId}/levels

```Get all level events for a specific game.



### Python AI Service (Analytics)#### GET /api/events/economy

Get all economy and transaction events.

**Base URL**: `http://localhost:8000` or `https://paime-analytics.up.railway.app`

#### GET /api/events/analytics/summary

| Endpoint | Method | Description |Get high-level analytics summary including:

|----------|--------|-------------|- Total users

| `/health` | GET | Health check |- Active users (24h, 7d)

| `/analytics/overview` | GET | Complete metrics |- Event counts by type

| `/analytics/churn` | GET | Churn predictions |- Total revenue (IAP + Ads)

| `/analytics/levels` | GET | Level analysis |

| `/analytics/users/segments` | GET | User segmentation |## 🗄️ Data Model

| `/analytics/users/{id}` | GET | Individual user |

| `/analytics/recommendations` | GET | AI recommendations |### Global Event Parameters

| `/analytics/stats` | GET | Raw statistics |Every event includes these common parameters:

- `userId` - Unique user identifier

---- `deviceId` - Device identifier

- `deviceModel` - Device model (e.g., "iPhone 14 Pro")

## 📊 Dashboard- `osVersion` - OS version (e.g., "iOS 17.1")

- `platform` - Platform (iOS, Android, Windows, WebGL)

### Access- `appVersion` - Game version

- `timestamp` - Event timestamp (UTC)

- **Local**: http://localhost:8050- `sessionId` - Current session identifier

- **Railway**: https://paime-dashboard.up.railway.app- `sessionDuration` - Session duration in milliseconds



### Features### User Profile

Automatically maintained user profile with:

**Metrics Cards**:- First seen / last seen timestamps

- Total Users- Total events count

- Daily Active Users (DAU)- Total sessions count

- Average Session Duration- Current device and platform info

- Total Revenue- App version

- Day 1 Retention

- Total Events### Event Collections

Events are stored in separate MongoDB collections:

**Charts**:- `users` - User profiles

- User Activity Trends (DAU/WAU/MAU)- `game_events` - Game session events

- Platform Distribution- `level_events` - Level progression events

- Level Difficulty Heatmap- `economy_events` - Transaction events

- Level Progression Funnel- `mission_events` - Mission/quest events

- Drop-off Levels- `ads_events` - Advertisement events

- Churn Risk Distribution- `ui_interaction_events` - UI events

- High-Risk Users

- AI Recommendations## 🎯 Event Types Reference



---### Session Events

- `SESSION_START`, `SESSION_END`, `SESSION_TIMEOUT`

## 🗄️ Data Population- `SESSION_PAUSE`, `SESSION_RESUME`, `SESSION_INTERRUPT`



### Quick Test Data### Level Events

- `LEVEL_START`, `LEVEL_COMPLETE`, `LEVEL_FAIL`, `LEVEL_QUIT`

```bash- `LEVEL_RESTART`, `LEVEL_UNLOCK`, `LEVEL_CHECKPOINT`, `LEVEL_SKIP`

# Generate 10 users, 40K+ events

python populate_comprehensive_data.py### Game Events

```- `GAME_START`, `GAME_END`, `GAME_COMPLETE`

- `GAME_BOSS_DEFEAT`, `GAME_BOSS_FAIL`

### User Archetypes- `GAME_ITEM_COLLECT`, `GAME_ITEM_USE`

- `GAME_PLAYER_DEATH`, `GAME_PLAYER_RESPAWN`

The script generates realistic user profiles:- `GAME_SCORE_UPDATE`, `GAME_HIGH_SCORE`

- **Whale** (5%): High spenders, 100-200 sessions- `GAME_POWERUP_USE`, `GAME_POWERUP_EXPIRE`

- **Engaged** (25%): Active players, 80-150 sessions

- **Casual** (40%): Regular players, 30-80 sessions### Economy Events

- **At-Risk** (20%): Declining activity, 10-30 sessions- `ECONOMY_CURRENCY_PURCHASE`, `ECONOMY_CURRENCY_SPEND`, `ECONOMY_CURRENCY_EARN`

- **Dormant** (10%): Inactive, 5-15 sessions- `ECONOMY_IAP_PURCHASE`, `ECONOMY_IAP_FAIL`

- `ECONOMY_SHOP_VIEW`, `ECONOMY_UPGRADE`, `ECONOMY_UNLOCK`

### Data Generated

### Social Events

- 10 user profiles with demographics- `SOCIAL_INVITE_SENT`, `SOCIAL_INVITE_ACCEPTED`, `SOCIAL_SHARE`

- 40,000+ events across 7 types- `SOCIAL_GUILD_JOIN`, `SOCIAL_GUILD_LEAVE`

- 15 game levels- `SOCIAL_MULTIPLAYER_JOIN`, `SOCIAL_MULTIPLAYER_WIN`, `SOCIAL_MULTIPLAYER_LOSE`

- Revenue transactions

- 30-day activity history### Achievement Events

- `ACHIEVEMENT_UNLOCK`, `ACHIEVEMENT_PROGRESS`, `ACHIEVEMENT_LEVEL_UP`

---

### Ad Events

## 📁 Project Structure- `AD_LOADED`, `AD_SHOWN`, `AD_COMPLETED`, `AD_CLOSED`

- `AD_CLICK`, `AD_REVENUE`, `AD_LOAD_FAIL`

```- `AD_REWARDED_SHOWN`, `AD_REWARDED_COMPLETE`

PlayMetric/

├── backend-java/              # Java Spring Boot API### UI Events

│   ├── src/- `UI_BUTTON_CLICK`, `UI_MENU_OPEN`, `UI_MENU_CLOSE`

│   │   └── main/- `UI_SETTINGS_OPEN`, `UI_SETTINGS_CHANGE`

│   │       ├── java/org/playmetric/

│   │       │   ├── Main.java### Tutorial Events

│   │       │   ├── config/- `TUTORIAL_START`, `TUTORIAL_COMPLETE`, `TUTORIAL_SKIP`

│   │       │   ├── controller/

│   │       │   ├── model/### Performance Events

│   │       │   ├── repository/- `PERFORMANCE_ERROR`, `PERFORMANCE_CRASH`, `PERFORMANCE_LOW_FPS`

│   │       │   └── service/

│   │       └── resources/## 🔧 Configuration

│   │           └── application.yml

│   ├── pom.xml### Application Properties

│   └── DockerfileConfigure in `application.yml`:

│

├── backend-python/            # Python AI Service```yaml

│   ├── app/spring:

│   │   ├── main.py           # FastAPI app  data:

│   │   ├── unified_main.py   # Unified FastAPI + Dash    mongodb:

│   │   ├── database.py       # MongoDB connection      uri: "mongodb://localhost:27017/playmetric"

│   │   ├── models/           # ML models

│   │   │   ├── churn_predictor.pyserver:

│   │   │   └── level_analyzer.py  port: 8080

│   │   ├── services/         # Analytics services

│   │   │   ├── analytics_engine.pyspringdoc:

│   │   │   └── game_recommendations.py  api-docs:

│   │   └── dashboard/        # Dash dashboard    path: /api-docs

│   │       └── dashboard.py  swagger-ui:

│   ├── requirements.txt    path: /swagger-ui.html

│   ├── Dockerfile           # API + Dashboard unified

│   └── Dockerfile.dashboard # Dashboard only (Railway)logging:

│  level:

├── populate_comprehensive_data.py  # Data generator    org.playmetric: DEBUG

├── docker-compose.yml        # Local development```

├── railway.json              # Railway configuration

└── README.md                 # This file## 🐳 Docker Deployment

```

### Using Docker Compose

---```bash

docker-compose up -d

## 🔧 Configuration```



### Environment VariablesThe `docker-compose.yml` includes:

- PlayMetric application

#### Java Backend- MongoDB database

```bash- Network configuration

SPRING_DATA_MONGODB_URI=mongodb://user:pass@host:port/dbname?authSource=admin

SERVER_PORT=8080## 📈 Analytics & AI Integration

```

### Data Export for AI/ML

#### Python AI ServiceEvents are structured for easy export to:

```bash- Pandas DataFrames (Python)

MONGODB_URI=mongodb://user:pass@host:port- CSV/JSON for ML pipelines

DATABASE_NAME=playmetric- BigQuery, Snowflake, etc.

PORT=8000

```### Example: Export for Python Analysis

```python

#### Dashboardimport requests

```bashimport pandas as pd

MONGODB_URI=mongodb://user:pass@host:port

DATABASE_NAME=playmetric# Get all level events

API_URL=http://localhost:8000  # Or Railway URLresponse = requests.get('http://localhost:8080/api/events/level')

PORT=8050level_events = response.json()

```

# Convert to DataFrame

---df = pd.DataFrame(level_events)



## 🧪 Testing# Analyze level difficulty

difficulty_analysis = df.groupby('levelId').agg({

### Test API Endpoints    'completed': 'mean',  # Completion rate

    'attemptCount': 'mean',  # Average attempts

```bash    'levelDuration': 'mean'  # Average time

# Java API health})

curl http://localhost:8080/actuator/health

print(difficulty_analysis)

# Python API health```

curl http://localhost:8000/health

### Use Cases for AI Analysis

# Get analytics overview1. **Level Difficulty Prediction** - Predict optimal difficulty curves

curl http://localhost:8000/analytics/overview2. **Churn Prediction** - Identify users at risk of churning

3. **Monetization Optimization** - Optimize IAP placement and pricing

# Get churn analysis4. **Player Segmentation** - Cluster users by behavior patterns

curl http://localhost:8000/analytics/churn?limit=105. **Content Recommendation** - Suggest levels or content

6. **A/B Testing** - Compare feature variants

# Get level analysis

curl http://localhost:8000/analytics/levels## 🧪 Testing



# Check data statisticsRun tests with:

curl http://localhost:8000/analytics/stats```bash

```mvn test

```

### Send Test Event

### Example Test Event

```bash```bash

curl -X POST http://localhost:8080/api/events \curl -X POST http://localhost:8080/api/events \

  -H "Content-Type: application/json" \  -H "Content-Type: application/json" \

  -d '{  -d '{

    "globalParams": {    "globalParams": {

      "userId": "test_user_001",      "userId": "test_user_1",

      "deviceId": "device123",      "deviceId": "test_device",

      "platform": "ANDROID",      "platform": "iOS",

      "sessionId": "session456",      "appVersion": "1.0.0",

      "timestamp": "2025-10-14T12:00:00Z"      "sessionId": "test_session"

    },    },

    "eventType": "LEVEL_COMPLETE",    "eventType": "LEVEL_COMPLETE",

    "levelId": 1,    "levelId": "level_1",

    "score": 1500,    "completed": true,

    "stars": 3,    "score": 1000

    "completed": true,  }'

    "timeTaken": 120```

  }'

```## 👥 Authors



---- **Vishnu Garg** - [@vishnugarg323](https://github.com/vishnugarg323)



## 🐛 Troubleshooting## 📞 Support



### Dashboard shows no dataFor questions or support:

**Solution**: Run `python populate_comprehensive_data.py`- Create an issue on GitHub

- Documentation: http://localhost:8080/swagger-ui.html

### Services won't start

**Solution**: Check ports 8080, 8000, 8050 are not in use## 🗺️ Roadmap

```bash

netstat -ano | findstr :8080- [ ] Real-time dashboards

netstat -ano | findstr :8000- [ ] Advanced analytics endpoints

netstat -ano | findstr :8050- [ ] Machine learning model integration

```- [ ] Multi-tenant support

- [ ] Data retention policies

### MongoDB connection error- [ ] Event batching for high-volume scenarios

**Solution**: Verify MongoDB URI in environment variables- [ ] WebSocket support for real-time updates



### Railway deployment fails---

**Solution**: 

- Ensure Dockerfile exists in service root directory**Built with ❤️ for game developers and data scientists**

- Check environment variables are set
- Verify Railway service is pointing to correct directory

---

## 📈 Roadmap

- [ ] Real-time event streaming
- [ ] User authentication & authorization
- [ ] Export analytics to PDF/CSV
- [ ] Email alerts for critical issues
- [ ] Mobile app support
- [ ] Multi-game support
- [ ] A/B testing framework
- [ ] Player lifetime value prediction
- [ ] Sentiment analysis from feedback

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Vishnu Garg**
- GitHub: [@vishnugarg323](https://github.com/vishnugarg323)
- Repository: [PlayMetric](https://github.com/vishnugarg323)

---

## 🙏 Acknowledgments

- Spring Boot for the robust Java framework
- FastAPI for the lightning-fast Python API
- Plotly Dash for beautiful interactive dashboards
- Railway for seamless deployment
- MongoDB for flexible data storage

---

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review API documentation in Swagger UI

---

**Built with ❤️ for game developers who want to understand their players better.**

🎮 Happy Gaming! 🚀
