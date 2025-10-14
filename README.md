# PlayMetric - Game Analytics Platform

[![Java](https://img.shields.io/badge/Java-21-orange.svg)](https://openjdk.java.net/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5.0-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)](https://www.mongodb.com/)

A comprehensive game analytics platform designed to track, analyze, and provide insights into game events for AI-driven analysis. Built with Spring Boot 3.5.0 and Java 21, optimized for Unity game integration and AI/ML analytics.

## 🎯 Overview

PlayMetric is a production-ready game analytics API that provides:

- **Unified Event Tracking**: Single POST endpoint for all event types
- **Automatic User Management**: User profiles created and updated automatically
- **AI-Ready Data Structure**: Optimized for machine learning and data analysis
- **Comprehensive Event Types**: 100+ predefined event types covering all game scenarios
- **Rich Analytics Endpoints**: RESTful APIs for data retrieval and analysis
- **Full Documentation**: OpenAPI/Swagger documentation for all endpoints

## 🚀 Key Features

### Event Tracking
- **Single POST Endpoint**: `/api/events` - One endpoint for all event types
- **Global Parameters**: Consistent user, device, and session tracking across all events
- **Automatic Routing**: Events automatically routed to appropriate collections
- **Real-time Processing**: Instant event recording and user profile updates

### Event Categories
1. **Session Events** - Game sessions, pause/resume tracking
2. **Level Events** - Level progression, completion, difficulty metrics
3. **Game Events** - Gameplay mechanics, scores, achievements
4. **Economy Events** - IAP, virtual currency, transactions
5. **Social Events** - Multiplayer, guilds, sharing
6. **Achievement Events** - Unlocks, progress, milestones
7. **Ad Events** - Ad impressions, revenue, engagement
8. **UI Events** - User interface interactions, navigation
9. **Performance Events** - Errors, crashes, performance metrics

### Analytics Capabilities
- User retention and churn analysis
- Level difficulty calibration
- Monetization optimization
- Session engagement metrics
- Cross-platform analytics
- Cohort analysis
- Revenue tracking (IAP + Ads)

## 📋 Requirements

- **Java**: JDK 21 or higher
- **Maven**: 3.6+ (for building)
- **MongoDB**: 4.4+ (for data storage)
- **Memory**: Minimum 512MB RAM

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/vishnugarg323/PlayMetric.git
cd PlayMetric
```

### 2. Configure MongoDB
Edit `src/main/resources/application.yml`:
```yaml
spring:
  data:
    mongodb:
      uri: "mongodb://your-mongodb-host:27017/playmetric"
```

### 3. Build the Project
```bash
mvn clean package
```

### 4. Run the Application
```bash
java -jar target/playmetric-parent-1.0-SNAPSHOT.jar
```

The application will start on `http://localhost:8080`

## 📚 API Documentation

### Swagger UI
Access the interactive API documentation at:
```
http://localhost:8080/swagger-ui.html
```

### OpenAPI Spec
Download the OpenAPI specification at:
```
http://localhost:8080/api-docs
```

## 🎮 Unity Integration

### Sending Events from Unity

```csharp
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;

public class PlayMetricClient : MonoBehaviour
{
    private const string API_URL = "http://your-server:8080/api/events";
    private string userId;
    private string sessionId;

    void Start()
    {
        userId = SystemInfo.deviceUniqueIdentifier;
        sessionId = System.Guid.NewGuid().ToString();
        
        // Send session start event
        SendSessionStart();
    }

    // Send a level complete event
    public void OnLevelComplete(string levelId, int score, int stars)
    {
        var eventData = new
        {
            globalParams = new
            {
                userId = userId,
                deviceId = SystemInfo.deviceUniqueIdentifier,
                deviceModel = SystemInfo.deviceModel,
                osVersion = SystemInfo.operatingSystem,
                platform = Application.platform.ToString(),
                appVersion = Application.version,
                sessionId = sessionId,
                sessionDuration = (long)(Time.realtimeSinceStartup * 1000)
            },
            eventType = "LEVEL_COMPLETE",
            gameId = "my_awesome_game",
            levelId = levelId,
            completed = true,
            score = score,
            starsEarned = stars,
            levelDuration = 120000
        };

        StartCoroutine(SendEventCoroutine(eventData));
    }

    // Send economy purchase event
    public void OnPurchase(string itemId, double price)
    {
        var eventData = new
        {
            globalParams = GetGlobalParams(),
            eventType = "ECONOMY_IAP_PURCHASE",
            transactionId = System.Guid.NewGuid().ToString(),
            itemId = itemId,
            realMoneyValue = price,
            currencyType = "USD"
        };

        StartCoroutine(SendEventCoroutine(eventData));
    }

    private object GetGlobalParams()
    {
        return new
        {
            userId = userId,
            deviceId = SystemInfo.deviceUniqueIdentifier,
            deviceModel = SystemInfo.deviceModel,
            osVersion = SystemInfo.operatingSystem,
            platform = Application.platform.ToString(),
            appVersion = Application.version,
            sessionId = sessionId,
            sessionDuration = (long)(Time.realtimeSinceStartup * 1000)
        };
    }

    private IEnumerator SendEventCoroutine(object eventData)
    {
        string jsonData = JsonUtility.ToJson(eventData);
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);

        using (UnityWebRequest request = new UnityWebRequest(API_URL, "POST"))
        {
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("Event sent successfully!");
            }
            else
            {
                Debug.LogError($"Error sending event: {request.error}");
            }
        }
    }
}
```

## 📊 API Endpoints

### Event Recording

#### POST /api/events
Record any type of game event.

**Request Body:**
```json
{
  "globalParams": {
    "userId": "user_12345",
    "deviceId": "device_abc",
    "deviceModel": "iPhone 14 Pro",
    "osVersion": "iOS 17.1",
    "platform": "iOS",
    "appVersion": "1.0.0",
    "sessionId": "session_xyz",
    "sessionDuration": 1800000
  },
  "eventType": "LEVEL_COMPLETE",
  "gameId": "adventure_mode",
  "levelId": "level_1_1",
  "completed": true,
  "score": 1500,
  "starsEarned": 3
}
```

### Data Retrieval

#### GET /api/events
Get all events grouped by type.

#### GET /api/events/users
Get all users with activity metrics.

#### GET /api/events/users/{userId}
Get detailed information for a specific user.

#### GET /api/events/users/{userId}/events
Get all events for a specific user across all types.

#### GET /api/events/game
Get all game session events.

#### GET /api/events/level
Get all level progression events.

#### GET /api/events/level/{levelId}
Get all events for a specific level.

#### GET /api/events/game/{gameId}/levels
Get all level events for a specific game.

#### GET /api/events/economy
Get all economy and transaction events.

#### GET /api/events/analytics/summary
Get high-level analytics summary including:
- Total users
- Active users (24h, 7d)
- Event counts by type
- Total revenue (IAP + Ads)

## 🗄️ Data Model

### Global Event Parameters
Every event includes these common parameters:
- `userId` - Unique user identifier
- `deviceId` - Device identifier
- `deviceModel` - Device model (e.g., "iPhone 14 Pro")
- `osVersion` - OS version (e.g., "iOS 17.1")
- `platform` - Platform (iOS, Android, Windows, WebGL)
- `appVersion` - Game version
- `timestamp` - Event timestamp (UTC)
- `sessionId` - Current session identifier
- `sessionDuration` - Session duration in milliseconds

### User Profile
Automatically maintained user profile with:
- First seen / last seen timestamps
- Total events count
- Total sessions count
- Current device and platform info
- App version

### Event Collections
Events are stored in separate MongoDB collections:
- `users` - User profiles
- `game_events` - Game session events
- `level_events` - Level progression events
- `economy_events` - Transaction events
- `mission_events` - Mission/quest events
- `ads_events` - Advertisement events
- `ui_interaction_events` - UI events

## 🎯 Event Types Reference

### Session Events
- `SESSION_START`, `SESSION_END`, `SESSION_TIMEOUT`
- `SESSION_PAUSE`, `SESSION_RESUME`, `SESSION_INTERRUPT`

### Level Events
- `LEVEL_START`, `LEVEL_COMPLETE`, `LEVEL_FAIL`, `LEVEL_QUIT`
- `LEVEL_RESTART`, `LEVEL_UNLOCK`, `LEVEL_CHECKPOINT`, `LEVEL_SKIP`

### Game Events
- `GAME_START`, `GAME_END`, `GAME_COMPLETE`
- `GAME_BOSS_DEFEAT`, `GAME_BOSS_FAIL`
- `GAME_ITEM_COLLECT`, `GAME_ITEM_USE`
- `GAME_PLAYER_DEATH`, `GAME_PLAYER_RESPAWN`
- `GAME_SCORE_UPDATE`, `GAME_HIGH_SCORE`
- `GAME_POWERUP_USE`, `GAME_POWERUP_EXPIRE`

### Economy Events
- `ECONOMY_CURRENCY_PURCHASE`, `ECONOMY_CURRENCY_SPEND`, `ECONOMY_CURRENCY_EARN`
- `ECONOMY_IAP_PURCHASE`, `ECONOMY_IAP_FAIL`
- `ECONOMY_SHOP_VIEW`, `ECONOMY_UPGRADE`, `ECONOMY_UNLOCK`

### Social Events
- `SOCIAL_INVITE_SENT`, `SOCIAL_INVITE_ACCEPTED`, `SOCIAL_SHARE`
- `SOCIAL_GUILD_JOIN`, `SOCIAL_GUILD_LEAVE`
- `SOCIAL_MULTIPLAYER_JOIN`, `SOCIAL_MULTIPLAYER_WIN`, `SOCIAL_MULTIPLAYER_LOSE`

### Achievement Events
- `ACHIEVEMENT_UNLOCK`, `ACHIEVEMENT_PROGRESS`, `ACHIEVEMENT_LEVEL_UP`

### Ad Events
- `AD_LOADED`, `AD_SHOWN`, `AD_COMPLETED`, `AD_CLOSED`
- `AD_CLICK`, `AD_REVENUE`, `AD_LOAD_FAIL`
- `AD_REWARDED_SHOWN`, `AD_REWARDED_COMPLETE`

### UI Events
- `UI_BUTTON_CLICK`, `UI_MENU_OPEN`, `UI_MENU_CLOSE`
- `UI_SETTINGS_OPEN`, `UI_SETTINGS_CHANGE`

### Tutorial Events
- `TUTORIAL_START`, `TUTORIAL_COMPLETE`, `TUTORIAL_SKIP`

### Performance Events
- `PERFORMANCE_ERROR`, `PERFORMANCE_CRASH`, `PERFORMANCE_LOW_FPS`

## 🔧 Configuration

### Application Properties
Configure in `application.yml`:

```yaml
spring:
  data:
    mongodb:
      uri: "mongodb://localhost:27017/playmetric"

server:
  port: 8080

springdoc:
  api-docs:
    path: /api-docs
  swagger-ui:
    path: /swagger-ui.html

logging:
  level:
    org.playmetric: DEBUG
```

## 🐳 Docker Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

The `docker-compose.yml` includes:
- PlayMetric application
- MongoDB database
- Network configuration

## 📈 Analytics & AI Integration

### Data Export for AI/ML
Events are structured for easy export to:
- Pandas DataFrames (Python)
- CSV/JSON for ML pipelines
- BigQuery, Snowflake, etc.

### Example: Export for Python Analysis
```python
import requests
import pandas as pd

# Get all level events
response = requests.get('http://localhost:8080/api/events/level')
level_events = response.json()

# Convert to DataFrame
df = pd.DataFrame(level_events)

# Analyze level difficulty
difficulty_analysis = df.groupby('levelId').agg({
    'completed': 'mean',  # Completion rate
    'attemptCount': 'mean',  # Average attempts
    'levelDuration': 'mean'  # Average time
})

print(difficulty_analysis)
```

### Use Cases for AI Analysis
1. **Level Difficulty Prediction** - Predict optimal difficulty curves
2. **Churn Prediction** - Identify users at risk of churning
3. **Monetization Optimization** - Optimize IAP placement and pricing
4. **Player Segmentation** - Cluster users by behavior patterns
5. **Content Recommendation** - Suggest levels or content
6. **A/B Testing** - Compare feature variants

## 🧪 Testing

Run tests with:
```bash
mvn test
```

### Example Test Event
```bash
curl -X POST http://localhost:8080/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "globalParams": {
      "userId": "test_user_1",
      "deviceId": "test_device",
      "platform": "iOS",
      "appVersion": "1.0.0",
      "sessionId": "test_session"
    },
    "eventType": "LEVEL_COMPLETE",
    "levelId": "level_1",
    "completed": true,
    "score": 1000
  }'
```

## 👥 Authors

- **Vishnu Garg** - [@vishnugarg323](https://github.com/vishnugarg323)

## 📞 Support

For questions or support:
- Create an issue on GitHub
- Documentation: http://localhost:8080/swagger-ui.html

## 🗺️ Roadmap

- [ ] Real-time dashboards
- [ ] Advanced analytics endpoints
- [ ] Machine learning model integration
- [ ] Multi-tenant support
- [ ] Data retention policies
- [ ] Event batching for high-volume scenarios
- [ ] WebSocket support for real-time updates

---

**Built with ❤️ for game developers and data scientists**
