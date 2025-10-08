# PlayMetric — API Reference & Deployment Guide

This README documents the HTTP API exposed by the PlayMetric microservice, how to test it locally, and recommended steps to deploy it to the cloud (Docker Hub + AWS ECS Fargate, Azure App Service for Containers, and Google Cloud Run).

## Quick status
- Service base URL (local Docker): http://localhost:8080
- OpenAPI (JSON): `/api-docs` — http://localhost:8080/api-docs
- Swagger UI: `/swagger-ui.html` — http://localhost:8080/swagger-ui.html

## Endpoints

Base path: `/api/events`

1) Record an event (generic)
   - Method: POST
   - URL: `/api/events`
   - Body: JSON representing one of the supported event types. The controller accepts different event record types (for example `GameEvent`, `LevelEvent`, `EconomyEvent`, `MissionEvent`, `AdsEvent`, `UIInteractionEvent`).
   - Success: 200 OK with stored document

   Example `GameEvent` payload (minimal):

   ```json
   {
     "id": null,
     "userId": "user-123",
     "deviceDetails": {
       "os": "Android",
       "osVersion": "14",
       "deviceModel": "Pixel"
     },
     "timestamp": "2025-10-08T12:00:00Z",
     "eventType": "GAME_START",
     "sessionId": "session-abc",
     "playingPattern": "casual",
     "sessionDuration": 120
   }
   ```

   Example `LevelEvent` payload (minimal):

   ```json
   {
     "id": null,
     "userId": "user-123",
     "deviceDetails": { "os": "iOS", "osVersion": "18", "deviceModel": "iPhone" },
     "timestamp": "2025-10-08T12:05:00Z",
     "eventType": "LEVEL_COMPLETE",
     "levelId": "level-2",
     "success": true
   }
   ```

2) Get game events by user
   - Method: GET
   - URL: `/api/events/game/user/{userId}`
   - Example: `GET /api/events/game/user/user-123`

3) Get level events by user
   - Method: GET
   - URL: `/api/events/level/user/{userId}`
   - Example: `GET /api/events/level/user/user-123`

Note: Additional repository-backed endpoints can be added similarly for economy/mission/ads/ui-interaction events.

## Test locally (manual)

Prerequisites:
- Docker and Docker Compose installed
- Service started via `docker-compose up -d` (root of this repo)

1) Verify Swagger/OpenAPI is available

```
# Open these in a browser or use curl
http://localhost:8080/swagger-ui.html
http://localhost:8080/api-docs
```

2) Send a POST to record an event (PowerShell / curl examples)

PowerShell (Windows):

```powershell
$body = @'
{
  "id": null,
  "userId": "tester-1",
  "deviceDetails": {"os":"Android","osVersion":"14","deviceModel":"Pixel"},
  "timestamp": "2025-10-08T12:00:00Z",
  "eventType": "GAME_START",
  "sessionId": "sess-1",
  "playingPattern": "casual",
  "sessionDuration": 42
}
'@

Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/events -Body $body -ContentType 'application/json'
```

curl (Linux/macOS/WSL):

```bash
curl -X POST http://localhost:8080/api/events \
  -H 'Content-Type: application/json' \
  -d @gameevent.json
```

3) Query events

```bash
curl http://localhost:8080/api/events/game/user/tester-1
```

4) Inspect MongoDB directly (Docker)

```powershell
docker exec -it playmetric-mongodb mongosh
use playmetric
show collections
db.getCollectionNames()
db.gameEvent.find().pretty()  # collection name depends on repository mapping
```

If collection names differ, list all collections and inspect them to find saved documents.

## Minimal Java tester (one-off)

You can quickly create and run a tiny Java program that posts events using the JDK HttpClient. Example `ApiTester.java`:

```java
// Minimal example (requires Java 11+)
import java.net.http.*;
import java.net.*;
import java.time.*;
import java.nio.file.*;

public class ApiTester {
  public static void main(String[] args) throws Exception {
    var client = HttpClient.newHttpClient();
    var json = Files.readString(Path.of("sample-event.json"));
    var req = HttpRequest.newBuilder()
      .uri(URI.create("http://localhost:8080/api/events"))
      .header("Content-Type", "application/json")
      .POST(HttpRequest.BodyPublishers.ofString(json))
      .build();
    var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
    System.out.println(resp.statusCode());
    System.out.println(resp.body());
  }
}
```

Save `sample-event.json` with a payload from above and run via `javac ApiTester.java && java ApiTester`.

## Deploy to cloud — recommended approaches

Below are concise, practical choices. Pick one based on your cloud provider preference.

Prerequisite common steps (for container based deploy):
1. Build the image locally or via CI: `docker build -t your-username/playmetric:latest .`
2. Push to a registry (Docker Hub / AWS ECR / GCR / ACR).

### Option A — Docker Hub + AWS ECS (Fargate)

1) Tag and push to Docker Hub:

```powershell
docker login
docker build -t <dockerhub-username>/playmetric:latest .
docker push <dockerhub-username>/playmetric:latest
```

2) Create an ECS cluster and a Fargate service using the pushed image. Use the AWS Console or `aws cli` with a task definition referencing the image. Ensure the task has the environment variable `SPRING_DATA_MONGODB_URI` pointing to your MongoDB (hosted or Atlas). Open port 8080 in the service's security group.

3) For production, use AWS RDS/Amazon DocumentDB or MongoDB Atlas for managed MongoDB.

### Option B — Azure App Service for Containers

1) Push your image to Azure Container Registry (ACR) or Docker Hub.
2) Create an App Service (Linux) and choose "Docker Container". Provide image path and set environment variables (SPRING_DATA_MONGODB_URI).

### Option C — Google Cloud Run

1) Tag and push to Google Container Registry or Artifact Registry.
2) Deploy with `gcloud run deploy --image=gcr.io/PROJECT/playmetric --platform=managed --region=... --allow-unauthenticated` and set environment variables.

## Recommended production considerations
- Use a managed MongoDB (Atlas, DocumentDB, ACR) instead of containerized local MongoDB.
- Add readiness/liveness probes.
- Configure logging (structured JSON) and a metrics endpoint.
- Secure the API endpoints (authentication, rate limiting).
- Use a CI pipeline to build, test, tag, and push images (GitHub Actions, GitLab CI, etc.).

## Troubleshooting
- If Swagger UI doesn't load, check application logs: `docker logs playmetric-service --follow`.
- If the container fails with `no main manifest attribute`, ensure the Spring Boot Maven plugin is configured and JAR is runnable (the repository already contains this configuration after recent edits).
- If you see class-file version errors, ensure Docker runtime JDK version matches compilation target.

---

If you want, I can also:
- Create the small `playmetric-api-tester` Maven project inside the repo and run it to post a sample event and verify storage automatically.
- Produce ready-to-run GitHub Actions workflow to build, test, and push the Docker image to Docker Hub or ECR.

Tell me which follow-up you'd like and I'll implement it next.

## One-click / cheap public deployment (recommended)

For a low-cost public deployment where people outside your laptop can hit the API, the simplest path is:

1) Managed MongoDB: Create a free-tier cluster on MongoDB Atlas and get the connection string. Example:

```
mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/playmetric?retryWrites=true&w=majority
```

2) Container registry: Push your image to Docker Hub (see CI workflow added in `.github/workflows/docker-publish.yml`).

3) Host the service on Render (free starter tier) or Fly.io / Railway / Google Cloud Run free tier.

Render steps (quick):
- Create a Render account
- Create a new "Web Service" and select "Dockerfile"
- Set the Docker image build context to this repo (Render will build it). If you pushed to Docker Hub you can select the image instead.
- Set environment variable `SPRING_DATA_MONGODB_URI` to your Atlas URI.
- Expose port 8080

Optional `render.yaml` manifest (Render will accept this or you can configure via UI):

```yaml
services:
  - type: web
    name: playmetric
    env: docker
    plan: starter
    dockerfilePath: ./Dockerfile
    envVars:
      - key: SPRING_DATA_MONGODB_URI
        value: $SPRING_DATA_MONGODB_URI
```

After deployment, Render will provide a public URL. Test by calling `POST /api/events` against that URL.

### Quick checklist to make public deployment work
- Provision MongoDB Atlas and allow the host (Render / Cloud Run) IPs or 0.0.0.0/0 depending on Atlas setup.
- Set `SPRING_DATA_MONGODB_URI` in the host environment.
- Ensure any firewalls or security groups allow 8080 inbound to the service (Render handles this for you).

If you want, I can:
- Create the small Java tester subproject and run it locally to verify event storage now.
- Add the `render.yaml` file and a short `deploy-to-render.md` with exact UI steps and screenshots (text only).

