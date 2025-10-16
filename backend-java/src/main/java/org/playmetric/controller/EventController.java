package org.playmetric.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.playmetric.model.*;
import org.playmetric.repository.*;
import org.playmetric.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Main controller for game event tracking and analytics.
 * 
 * <p>This controller provides:
 * <ul>
 *   <li>Unified POST endpoint for all event types</li>
 *   <li>Automatic user creation and tracking</li>
 *   <li>Event routing to appropriate collections</li>
 *   <li>Comprehensive GET endpoints for analytics</li>
 * </ul>
 * 
 * <p>The API is designed for:
 * - Unity game clients to send events
 * - AI systems to retrieve data for analysis
 * - Dashboard applications to display analytics
 */
@RestController
@RequestMapping("/api/events")
@Tag(name = "Game Analytics API", description = "Comprehensive game event tracking and analytics APIs")
public class EventController {
    
    private static final Logger logger = LoggerFactory.getLogger(EventController.class);
    
    private final UserService userService;
    private final GameEventRepository gameEventRepository;
    private final LevelEventRepository levelEventRepository;
    private final EconomyEventRepository economyEventRepository;
    private final MissionEventRepository missionEventRepository;
    private final AdsEventRepository adsEventRepository;
    private final UIInteractionEventRepository uiInteractionEventRepository;

    public EventController(
        UserService userService,
        GameEventRepository gameEventRepository,
        LevelEventRepository levelEventRepository,
        EconomyEventRepository economyEventRepository,
        MissionEventRepository missionEventRepository,
        AdsEventRepository adsEventRepository,
        UIInteractionEventRepository uiInteractionEventRepository
    ) {
        this.userService = userService;
        this.gameEventRepository = gameEventRepository;
        this.levelEventRepository = levelEventRepository;
        this.economyEventRepository = economyEventRepository;
        this.missionEventRepository = missionEventRepository;
        this.adsEventRepository = adsEventRepository;
        this.uiInteractionEventRepository = uiInteractionEventRepository;
    }

    /**
     * Unified endpoint to record any type of game event.
     * This is the main endpoint that Unity clients should use.
     * 
     * The endpoint:
     * 1. Extracts global parameters from the payload
     * 2. Ensures user exists (creates if new, updates if existing)
     * 3. Routes event to appropriate collection based on eventType
     * 4. Returns the saved event
     */
    @PostMapping
    @Operation(
        summary = "Record a game event (Unified Endpoint)",
        description = """
            **Main endpoint for recording any game event.**
            
            Send a JSON payload containing:
            - `globalParams`: Common parameters (userId, deviceId, timestamp, sessionId, etc.)
            - `eventType`: Type of event (e.g., LEVEL_COMPLETE, GAME_START, ECONOMY_PURCHASE)
            - Event-specific data (e.g., levelId for level events, amount for economy events)
            
            The system will:
            1. Automatically create/update the user
            2. Route the event to the appropriate collection
            3. Return the saved event with generated ID
            
            **Example for Level Complete:**
            ```json
            {
              "globalParams": {
                "userId": "user_12345",
                "deviceId": "device_abc",
                "deviceModel": "iPhone 14 Pro",
                "osVersion": "iOS 17.1",
                "platform": "iOS",
                "appVersion": "1.0.0",
                "timestamp": "2025-10-14T12:00:00Z",
                "sessionId": "session_xyz",
                "sessionDuration": 1800000
              },
              "eventType": "LEVEL_COMPLETE",
              "gameId": "adventure_mode",
              "levelId": "level_1_1",
              "levelNumber": 1,
              "completed": true,
              "levelDuration": 120000,
              "score": 1500,
              "starsEarned": 3
            }
            ```
            """,
        requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
            description = "Event payload with global parameters and event-specific data",
            required = true,
            content = @Content(
                mediaType = "application/json",
                schema = @Schema(implementation = Map.class),
                examples = {
                    @ExampleObject(
                        name = "Level Complete Event",
                        value = """
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
                              "score": 1500
                            }
                            """
                    ),
                    @ExampleObject(
                        name = "Game Start Event",
                        value = """
                            {
                              "globalParams": {
                                "userId": "user_12345",
                                "deviceId": "device_abc",
                                "platform": "iOS",
                                "appVersion": "1.0.0",
                                "sessionId": "session_xyz"
                              },
                              "eventType": "SESSION_START",
                              "gameId": "adventure_mode"
                            }
                            """
                    ),
                    @ExampleObject(
                        name = "Economy Purchase Event",
                        value = """
                            {
                              "globalParams": {
                                "userId": "user_12345",
                                "platform": "Android",
                                "appVersion": "1.0.0",
                                "sessionId": "session_abc"
                              },
                              "eventType": "ECONOMY_IAP_PURCHASE",
                              "transactionId": "txn_12345",
                              "currencyType": "gold_coins",
                              "amount": 1000,
                              "realMoneyValue": 4.99
                            }
                            """
                    )
                }
            )
        ),
        responses = {
            @ApiResponse(
                responseCode = "200",
                description = "Event successfully recorded",
                content = @Content(schema = @Schema(implementation = Map.class))
            ),
            @ApiResponse(
                responseCode = "400",
                description = "Invalid event payload or missing required fields"
            ),
            @ApiResponse(
                responseCode = "500",
                description = "Internal server error"
            )
        }
    )
    public ResponseEntity<?> recordEvent(@RequestBody Map<String, Object> payload) {
        try {
            // Extract and validate global parameters
            @SuppressWarnings("unchecked")
            Map<String, Object> globalParamsMap = (Map<String, Object>) payload.get("globalParams");
            if (globalParamsMap == null) {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "Missing required field: globalParams"
                ));
            }

            GlobalEventParameters globalParams = extractGlobalParams(globalParamsMap);
            
            // Ensure user exists (create or update)
            userService.ensureUserExists(globalParams);
            
            // Extract event type
            String eventTypeStr = (String) payload.get("eventType");
            if (eventTypeStr == null) {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "Missing required field: eventType"
                ));
            }

            EventType eventType;
            try {
                eventType = EventType.valueOf(eventTypeStr);
            } catch (IllegalArgumentException e) {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "Invalid eventType: " + eventTypeStr,
                    "validTypes", Arrays.stream(EventType.values())
                        .map(Enum::name)
                        .collect(Collectors.toList())
                ));
            }

            // Route to appropriate handler based on event type
            Object savedEvent = routeEvent(eventType, globalParams, payload);
            
            logger.info("Event recorded: type={}, userId={}, eventId={}", 
                eventType, globalParams.userId(), 
                savedEvent instanceof GameEvent ? ((GameEvent) savedEvent).id() : "N/A");
            
            return ResponseEntity.ok(savedEvent);
            
        } catch (Exception e) {
            logger.error("Error recording event", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "error", "Failed to record event: " + e.getMessage()
            ));
        }
    }

    /**
     * Routes event to appropriate repository based on event type.
     */
    private Object routeEvent(EventType eventType, GlobalEventParameters globalParams, Map<String, Object> payload) {
        // Determine category from event type
        String eventName = eventType.name();
        
        if (eventName.startsWith("LEVEL_")) {
            return saveLevelEvent(eventType, globalParams, payload);
        } else if (eventName.startsWith("SESSION_") || eventName.startsWith("GAME_")) {
            return saveGameEvent(eventType, globalParams, payload);
        } else if (eventName.startsWith("ECONOMY_")) {
            return saveEconomyEvent(eventType, globalParams, payload);
        } else if (eventName.startsWith("MISSION_")) {
            return saveMissionEvent(eventType, globalParams, payload);
        } else if (eventName.startsWith("AD_")) {
            return saveAdsEvent(eventType, globalParams, payload);
        } else if (eventName.startsWith("UI_") || eventName.startsWith("TUTORIAL_")) {
            return saveUIInteractionEvent(eventType, globalParams, payload);
        } else {
            // Default to game event for unclassified events
            return saveGameEvent(eventType, globalParams, payload);
        }
    }

    private GameEvent saveGameEvent(EventType eventType, GlobalEventParameters globalParams, Map<String, Object> payload) {
        GameEvent event = new GameEvent(
            null, // MongoDB will auto-generate
            globalParams,
            eventType,
            getString(payload, "gameId"),
            getLong(payload, "score"),
            getLong(payload, "highScore"),
            getInteger(payload, "livesRemaining"),
            getInteger(payload, "healthRemaining"),
            getInteger(payload, "powerupsUsed"),
            getInteger(payload, "enemiesDefeated"),
            getInteger(payload, "bossesDefeated"),
            getString(payload, "playingPattern"),
            getString(payload, "additionalData")
        );
        return gameEventRepository.save(event);
    }

    private LevelEvent saveLevelEvent(EventType eventType, GlobalEventParameters globalParams, Map<String, Object> payload) {
        LevelEvent event = new LevelEvent(
            null,
            globalParams,
            eventType,
            getString(payload, "gameId"),
            getString(payload, "levelId"),
            getInteger(payload, "levelNumber"),
            getString(payload, "difficulty"),
            getInteger(payload, "attemptCount"),
            getBoolean(payload, "completed"),
            getLong(payload, "levelDuration"),
            getLong(payload, "score"),
            getInteger(payload, "starsEarned"),
            getBoolean(payload, "perfectCompletion"),
            getString(payload, "failReason"),
            getString(payload, "checkpointReached"),
            getInteger(payload, "hintsUsed"),
            getInteger(payload, "skipsUsed"),
            getInteger(payload, "itemsCollected"),
            getInteger(payload, "enemiesDefeated"),
            getInteger(payload, "damagesTaken"),
            getInteger(payload, "powerupsUsed"),
            getString(payload, "additionalData")
        );
        return levelEventRepository.save(event);
    }

    private EconomyEvent saveEconomyEvent(EventType eventType, GlobalEventParameters globalParams, Map<String, Object> payload) {
        EconomyEvent event = new EconomyEvent(
            null,
            globalParams,
            eventType,
            getString(payload, "transactionId"),
            getString(payload, "currencyType"),
            getDouble(payload, "amount"),
            getString(payload, "transactionType"),
            getDouble(payload, "realMoneyValue"),
            getString(payload, "itemId"),
            getString(payload, "itemName"),
            getString(payload, "itemCategory"),
            getDouble(payload, "balanceBefore"),
            getDouble(payload, "balanceAfter"),
            getString(payload, "source"),
            getString(payload, "additionalData")
        );
        return economyEventRepository.save(event);
    }

    private MissionEvent saveMissionEvent(EventType eventType, GlobalEventParameters globalParams, Map<String, Object> payload) {
        MissionEvent event = new MissionEvent(
            null,
            globalParams,
            eventType,
            getString(payload, "missionType"),
            getString(payload, "missionId"),
            getString(payload, "missionName"),
            getBoolean(payload, "completed"),
            getLong(payload, "missionDuration"),
            getInteger(payload, "progressPercentage"),
            getInteger(payload, "attemptCount"),
            getString(payload, "rewardType"),
            getDouble(payload, "rewardAmount"),
            getBoolean(payload, "rewardClaimed"),
            getString(payload, "additionalData")
        );
        return missionEventRepository.save(event);
    }

    private AdsEvent saveAdsEvent(EventType eventType, GlobalEventParameters globalParams, Map<String, Object> payload) {
        AdsEvent event = new AdsEvent(
            null,
            globalParams,
            eventType,
            getString(payload, "adEventType"),
            getDouble(payload, "revenue"),
            getString(payload, "adId"),
            getString(payload, "adNetwork"),
            getString(payload, "adPlacement"),
            getString(payload, "adFormat"),
            getLong(payload, "adDuration"),
            getBoolean(payload, "skipped"),
            getBoolean(payload, "clicked"),
            getString(payload, "rewardType"),
            getDouble(payload, "rewardAmount"),
            getString(payload, "additionalData")
        );
        return adsEventRepository.save(event);
    }

    private UIInteractionEvent saveUIInteractionEvent(EventType eventType, GlobalEventParameters globalParams, Map<String, Object> payload) {
        UIInteractionEvent event = new UIInteractionEvent(
            null,
            globalParams,
            eventType,
            getString(payload, "interactionType"),
            getString(payload, "screenName"),
            getString(payload, "elementId"),
            getString(payload, "elementName"),
            getString(payload, "elementType"),
            getString(payload, "previousScreen"),
            getString(payload, "details"),
            getString(payload, "additionalData")
        );
        return uiInteractionEventRepository.save(event);
    }

    // Helper methods to safely extract values from payload
    private GlobalEventParameters extractGlobalParams(Map<String, Object> map) {
        String timestampStr = (String) map.get("timestamp");
        Instant timestamp = timestampStr != null ? Instant.parse(timestampStr) : Instant.now();
        
        Long sessionDuration = null;
        Object durationObj = map.get("sessionDuration");
        if (durationObj != null) {
            sessionDuration = durationObj instanceof Number ? 
                ((Number) durationObj).longValue() : Long.parseLong(durationObj.toString());
        }

        return new GlobalEventParameters(
            (String) map.get("userId"),
            (String) map.get("deviceId"),
            (String) map.get("deviceModel"),
            (String) map.get("osVersion"),
            (String) map.get("platform"),
            (String) map.get("appVersion"),
            timestamp,
            (String) map.get("sessionId"),
            sessionDuration
        );
    }

    private String getString(Map<String, Object> map, String key) {
        Object value = map.get(key);
        return value != null ? value.toString() : null;
    }

    private Integer getInteger(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        if (value instanceof Number) return ((Number) value).intValue();
        try {
            return Integer.parseInt(value.toString());
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private Long getLong(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        if (value instanceof Number) return ((Number) value).longValue();
        try {
            return Long.parseLong(value.toString());
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private Double getDouble(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        if (value instanceof Number) return ((Number) value).doubleValue();
        try {
            return Double.parseDouble(value.toString());
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private Boolean getBoolean(Map<String, Object> map, String key) {
        Object value = map.get(key);
        if (value == null) return null;
        if (value instanceof Boolean) return (Boolean) value;
        return Boolean.parseBoolean(value.toString());
    }

    // ==================== GET ENDPOINTS ====================

    /**
     * Get all events grouped by type.
     */
    @GetMapping
    @Operation(
        summary = "Get all events grouped by type",
        description = "Returns all stored events organized by event type for comprehensive analytics"
    )
    public ResponseEntity<Map<String, Object>> getAllEvents() {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("game_events", gameEventRepository.findAll());
        response.put("level_events", levelEventRepository.findAll());
        response.put("economy_events", economyEventRepository.findAll());
        response.put("mission_events", missionEventRepository.findAll());
        response.put("ads_events", adsEventRepository.findAll());
        response.put("ui_interaction_events", uiInteractionEventRepository.findAll());
        response.put("total_events", 
            gameEventRepository.count() + 
            levelEventRepository.count() + 
            economyEventRepository.count() + 
            missionEventRepository.count() + 
            adsEventRepository.count() + 
            uiInteractionEventRepository.count()
        );
        return ResponseEntity.ok(response);
    }

    /**
     * Get all users.
     */
    @GetMapping("/users")
    @Operation(
        summary = "Get all users",
        description = "Returns a list of all users with their activity metrics"
    )
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(userService.getAllUsers());
    }

    /**
     * Get user by ID.
     */
    @GetMapping("/users/{userId}")
    @Operation(
        summary = "Get user by ID",
        description = "Returns detailed information about a specific user"
    )
    public ResponseEntity<?> getUserById(@PathVariable String userId) {
        return userService.getUserById(userId)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Get all events for a specific user.
     */
    @GetMapping("/users/{userId}/events")
    @Operation(
        summary = "Get all events for a user",
        description = "Returns all events across all types for a specific user"
    )
    public ResponseEntity<Map<String, Object>> getUserEvents(@PathVariable String userId) {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("user_id", userId);
        response.put("game_events", gameEventRepository.findAll().stream()
            .filter(e -> userId.equals(e.globalParams().userId()))
            .collect(Collectors.toList()));
        response.put("level_events", levelEventRepository.findAll().stream()
            .filter(e -> userId.equals(e.globalParams().userId()))
            .collect(Collectors.toList()));
        response.put("economy_events", economyEventRepository.findAll().stream()
            .filter(e -> userId.equals(e.globalParams().userId()))
            .collect(Collectors.toList()));
        response.put("mission_events", missionEventRepository.findAll().stream()
            .filter(e -> userId.equals(e.globalParams().userId()))
            .collect(Collectors.toList()));
        response.put("ads_events", adsEventRepository.findAll().stream()
            .filter(e -> userId.equals(e.globalParams().userId()))
            .collect(Collectors.toList()));
        response.put("ui_interaction_events", uiInteractionEventRepository.findAll().stream()
            .filter(e -> userId.equals(e.globalParams().userId()))
            .collect(Collectors.toList()));
        return ResponseEntity.ok(response);
    }

    /**
     * Get all game events.
     */
    @GetMapping("/game")
    @Operation(
        summary = "Get all game events",
        description = "Returns all game session and gameplay events"
    )
    public ResponseEntity<List<GameEvent>> getAllGameEvents() {
        return ResponseEntity.ok(gameEventRepository.findAll());
    }

    /**
     * Get all level events.
     */
    @GetMapping("/level")
    @Operation(
        summary = "Get all level events",
        description = "Returns all level progression events"
    )
    public ResponseEntity<List<LevelEvent>> getAllLevelEvents() {
        return ResponseEntity.ok(levelEventRepository.findAll());
    }

    /**
     * Get level events by level ID.
     */
    @GetMapping("/level/{levelId}")
    @Operation(
        summary = "Get events for a specific level",
        description = "Returns all events for a particular level across all users"
    )
    public ResponseEntity<List<LevelEvent>> getLevelEventsByLevelId(@PathVariable String levelId) {
        List<LevelEvent> events = levelEventRepository.findAll().stream()
            .filter(e -> levelId.equals(e.levelId()))
            .collect(Collectors.toList());
        return ResponseEntity.ok(events);
    }

    /**
     * Get level events by game ID.
     */
    @GetMapping("/game/{gameId}/levels")
    @Operation(
        summary = "Get all level events for a game",
        description = "Returns all level events associated with a specific game"
    )
    public ResponseEntity<List<LevelEvent>> getLevelEventsByGameId(@PathVariable String gameId) {
        List<LevelEvent> events = levelEventRepository.findAll().stream()
            .filter(e -> gameId.equals(e.gameId()))
            .collect(Collectors.toList());
        return ResponseEntity.ok(events);
    }

    /**
     * Get all economy events.
     */
    @GetMapping("/economy")
    @Operation(
        summary = "Get all economy events",
        description = "Returns all in-game economy and transaction events"
    )
    public ResponseEntity<List<EconomyEvent>> getAllEconomyEvents() {
        return ResponseEntity.ok(economyEventRepository.findAll());
    }

    /**
     * Health check endpoint for service handshake.
     */
    @GetMapping("/health")
    @Operation(
        summary = "Health check endpoint",
        description = "Simple health check endpoint used for service handshake and monitoring"
    )
    public ResponseEntity<Map<String, String>> healthCheck() {
        Map<String, String> health = new LinkedHashMap<>();
        health.put("status", "UP");
        health.put("service", "PlayMetric Event Tracking API");
        health.put("version", "1.0.0");
        health.put("timestamp", Instant.now().toString());
        return ResponseEntity.ok(health);
    }

    /**
     * Get analytics summary.
     */
    @GetMapping("/analytics/summary")
    @Operation(
        summary = "Get analytics summary",
        description = "Returns high-level analytics metrics including user counts, event counts, and activity stats"
    )
    public ResponseEntity<Map<String, Object>> getAnalyticsSummary() {
        Map<String, Object> summary = new LinkedHashMap<>();
        
        // User metrics
        long totalUsers = userService.getTotalUserCount();
        Instant dayAgo = Instant.now().minus(1, ChronoUnit.DAYS);
        Instant weekAgo = Instant.now().minus(7, ChronoUnit.DAYS);
        long activeUsersToday = userService.getActiveUsersSince(dayAgo).size();
        long activeUsersWeek = userService.getActiveUsersSince(weekAgo).size();
        
        summary.put("total_users", totalUsers);
        summary.put("active_users_24h", activeUsersToday);
        summary.put("active_users_7d", activeUsersWeek);
        
        // Event metrics
        summary.put("total_game_events", gameEventRepository.count());
        summary.put("total_level_events", levelEventRepository.count());
        summary.put("total_economy_events", economyEventRepository.count());
        summary.put("total_mission_events", missionEventRepository.count());
        summary.put("total_ads_events", adsEventRepository.count());
        summary.put("total_ui_events", uiInteractionEventRepository.count());
        
        // Calculate total revenue from ads
        double totalAdRevenue = adsEventRepository.findAll().stream()
            .mapToDouble(e -> e.revenue() != null ? e.revenue() : 0.0)
            .sum();
        summary.put("total_ad_revenue", totalAdRevenue);
        
        // Calculate total IAP revenue
        double totalIapRevenue = economyEventRepository.findAll().stream()
            .filter(e -> e.eventType().name().contains("IAP"))
            .mapToDouble(e -> e.realMoneyValue() != null ? e.realMoneyValue() : 0.0)
            .sum();
        summary.put("total_iap_revenue", totalIapRevenue);
        summary.put("total_revenue", totalAdRevenue + totalIapRevenue);
        
        return ResponseEntity.ok(summary);
    }
}
