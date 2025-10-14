# Unity Integration Guide for PlayMetric

This guide shows how to integrate PlayMetric game analytics into your Unity game.

## Setup

1. Copy the `PlayMetricClient.cs` script to your Unity project's `Assets/Scripts` folder
2. Attach the script to a persistent GameObject (e.g., GameManager)
3. Configure the API URL in the Inspector or in code

## Usage Examples

### 1. Session Tracking

```csharp
// In your game initialization
PlayMetricClient.Instance.SendSessionStart();

// When game closes
PlayMetricClient.Instance.SendSessionEnd();
```

### 2. Level Events

```csharp
// Level start
PlayMetricClient.Instance.SendLevelStart("level_1_1", "adventure_mode");

// Level complete
PlayMetricClient.Instance.SendLevelComplete(
    levelId: "level_1_1",
    gameId: "adventure_mode",
    score: 1500,
    stars: 3,
    duration: 120000, // milliseconds
    attemptCount: 1,
    completed: true
);

// Level failed
PlayMetricClient.Instance.SendLevelFail(
    levelId: "level_1_1",
    gameId: "adventure_mode",
    failReason: "out_of_time",
    attemptCount: 2
);
```

### 3. Economy Events

```csharp
// IAP Purchase
PlayMetricClient.Instance.SendIAPPurchase(
    itemId: "coin_pack_1000",
    itemName: "1000 Gold Coins",
    price: 4.99,
    currency: "USD"
);

// Currency spend
PlayMetricClient.Instance.SendCurrencySpend(
    currencyType: "gold",
    amount: 100,
    itemId: "health_potion",
    source: "shop"
);
```

### 4. Achievement Events

```csharp
PlayMetricClient.Instance.SendAchievementUnlock(
    achievementId: "first_win",
    achievementName: "First Victory"
);
```

### 5. Ad Events

```csharp
// Rewarded ad completed
PlayMetricClient.Instance.SendAdRewarded(
    adId: "ad_12345",
    adNetwork: "admob",
    rewardType: "extra_life",
    rewardAmount: 1
);
```

## Complete Example Script

Place this in `Assets/Scripts/PlayMetricExample.cs`:

```csharp
using UnityEngine;

public class PlayMetricExample : MonoBehaviour
{
    private void Start()
    {
        // Initialize session
        PlayMetricClient.Instance.SendSessionStart();
    }

    private void OnApplicationQuit()
    {
        // End session
        PlayMetricClient.Instance.SendSessionEnd();
    }

    public void OnLevelLoaded(string levelId)
    {
        PlayMetricClient.Instance.SendLevelStart(levelId, "main_game");
    }

    public void OnLevelCompleted(string levelId, int score, int stars)
    {
        PlayMetricClient.Instance.SendLevelComplete(
            levelId: levelId,
            gameId: "main_game",
            score: score,
            stars: stars,
            duration: (long)(Time.timeSinceLevelLoad * 1000),
            attemptCount: 1,
            completed: true
        );
    }

    public void OnPurchaseComplete(string itemId, double price)
    {
        PlayMetricClient.Instance.SendIAPPurchase(
            itemId: itemId,
            itemName: itemId,
            price: price,
            currency: "USD"
        );
    }
}
```

## Event Types Available

- Session: `SendSessionStart()`, `SendSessionEnd()`, `SendSessionPause()`, `SendSessionResume()`
- Level: `SendLevelStart()`, `SendLevelComplete()`, `SendLevelFail()`, `SendLevelQuit()`
- Economy: `SendIAPPurchase()`, `SendCurrencySpend()`, `SendCurrencyEarn()`
- Achievement: `SendAchievementUnlock()`, `SendAchievementProgress()`
- Ad: `SendAdShown()`, `SendAdCompleted()`, `SendAdRewarded()`
- UI: `SendUIInteraction()`
- Performance: `SendError()`, `SendCrash()`

## Best Practices

1. **Initialize Early**: Call `SendSessionStart()` in your game's initialization
2. **Track Everything**: More data = better insights
3. **Use Meaningful IDs**: Use consistent, descriptive IDs for levels, items, etc.
4. **Handle Failures**: The client handles network errors gracefully
5. **Test Locally**: Point to `http://localhost:8080` during development

## Configuration

Edit the `PlayMetricClient.cs` file to configure:

```csharp
// Development
private const string API_URL = "http://localhost:8080/api/events";

// Production
// private const string API_URL = "https://your-server.com/api/events";
```

## Troubleshooting

### Events Not Sending
- Check network connectivity
- Verify API URL is correct
- Check Unity console for error messages
- Ensure MongoDB is running

### User Not Being Created
- Check that `userId` is being set correctly
- Verify `globalParams` includes all required fields

### Build Errors
- Ensure you're using Unity 2020.3 or higher
- Check that `System.Text` namespace is available

## Testing

Test your integration:

1. Start your game
2. Trigger some events
3. Check the API: `http://localhost:8080/api/events`
4. View Swagger UI: `http://localhost:8080/swagger-ui.html`

## Support

For issues or questions:
- GitHub Issues: https://github.com/vishnugarg323/PlayMetric
- Documentation: http://localhost:8080/swagger-ui.html
