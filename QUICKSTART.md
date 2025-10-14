# 🚀 Quick Start Guide

Get PlayMetric up and running in 5 minutes!

## Prerequisites
- Java 21 installed
- MongoDB running (locally or remote)
- Maven installed

## Step 1: Configure MongoDB (30 seconds)

Edit `src/main/resources/application.yml`:

```yaml
spring:
  data:
    mongodb:
      uri: "mongodb://localhost:27017/playmetric"
```

Or use the existing Railway MongoDB connection that's already configured.

## Step 2: Build & Run (2 minutes)

```bash
# Build the project
mvn clean package -DskipTests

# Run the application
java -jar target/playmetric-parent-1.0-SNAPSHOT.jar
```

The application will start on **http://localhost:8080**

## Step 3: Test the API (1 minute)

### View the Documentation
Open in your browser:
```
http://localhost:8080/swagger-ui.html
```

### Send a Test Event

**Using curl:**
```bash
curl -X POST http://localhost:8080/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "globalParams": {
      "userId": "test_user_1",
      "deviceId": "test_device_123",
      "deviceModel": "iPhone 14 Pro",
      "osVersion": "iOS 17.1",
      "platform": "iOS",
      "appVersion": "1.0.0",
      "sessionId": "session_abc123",
      "sessionDuration": 300000
    },
    "eventType": "LEVEL_COMPLETE",
    "gameId": "my_game",
    "levelId": "level_1",
    "completed": true,
    "score": 1500,
    "starsEarned": 3,
    "levelDuration": 120000
  }'
```

**Using PowerShell:**
```powershell
$body = @{
    globalParams = @{
        userId = "test_user_1"
        deviceId = "test_device_123"
        platform = "iOS"
        appVersion = "1.0.0"
        sessionId = "session_abc123"
    }
    eventType = "LEVEL_COMPLETE"
    levelId = "level_1"
    completed = $true
    score = 1500
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/events" -Method Post -Body $body -ContentType "application/json"
```

## Step 4: View the Data (30 seconds)

### Get All Events
```bash
curl http://localhost:8080/api/events
```

### Get All Users
```bash
curl http://localhost:8080/api/events/users
```

### Get Analytics Summary
```bash
curl http://localhost:8080/api/events/analytics/summary
```

## What's Next?

### Integrate with Unity
1. Check out `UNITY_INTEGRATION.md`
2. Copy the Unity client code
3. Start sending events from your game!

### Explore the API
- Open Swagger UI: http://localhost:8080/swagger-ui.html
- Try different event types
- Query your data

### Set Up for Production
1. Configure production MongoDB
2. Set up proper logging
3. Deploy using Docker (see `docker-compose.yml`)
4. Set up monitoring

## Common Issues

### MongoDB Connection Error
- Make sure MongoDB is running: `mongod --version`
- Check the connection string in `application.yml`
- For Railway MongoDB, use the provided connection string

### Port Already in Use
Change the port in `application.yml`:
```yaml
server:
  port: 8081
```

### Build Errors
- Ensure Java 21 is installed: `java -version`
- Ensure Maven is installed: `mvn -version`
- Clean and rebuild: `mvn clean install`

## Available Event Types

Send any of these event types:

**Session**: `SESSION_START`, `SESSION_END`, `SESSION_PAUSE`, `SESSION_RESUME`

**Level**: `LEVEL_START`, `LEVEL_COMPLETE`, `LEVEL_FAIL`, `LEVEL_QUIT`

**Economy**: `ECONOMY_IAP_PURCHASE`, `ECONOMY_CURRENCY_SPEND`, `ECONOMY_CURRENCY_EARN`

**Achievement**: `ACHIEVEMENT_UNLOCK`, `ACHIEVEMENT_PROGRESS`

**Ads**: `AD_SHOWN`, `AD_COMPLETED`, `AD_REWARDED_COMPLETE`

And 80+ more! See `EventType.java` for the complete list.

## Example: Session Flow

```bash
# 1. Start session
curl -X POST http://localhost:8080/api/events -H "Content-Type: application/json" -d '{
  "globalParams": {"userId": "user_1", "platform": "iOS", "appVersion": "1.0", "sessionId": "s1"},
  "eventType": "SESSION_START", "gameId": "my_game"
}'

# 2. Start level
curl -X POST http://localhost:8080/api/events -H "Content-Type: application/json" -d '{
  "globalParams": {"userId": "user_1", "platform": "iOS", "appVersion": "1.0", "sessionId": "s1"},
  "eventType": "LEVEL_START", "gameId": "my_game", "levelId": "level_1"
}'

# 3. Complete level
curl -X POST http://localhost:8080/api/events -H "Content-Type: application/json" -d '{
  "globalParams": {"userId": "user_1", "platform": "iOS", "appVersion": "1.0", "sessionId": "s1"},
  "eventType": "LEVEL_COMPLETE", "gameId": "my_game", "levelId": "level_1", "completed": true, "score": 1000
}'

# 4. Check user stats
curl http://localhost:8080/api/events/users/user_1
```

## Get Help

- 📖 Read the full README.md
- 🎮 Check Unity integration guide
- 🐛 Report issues on GitHub
- 💬 Open Swagger UI for API details

**You're all set! Start tracking game events! 🎉**
