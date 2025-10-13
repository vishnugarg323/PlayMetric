package org.playmetric.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.playmetric.model.*;
import org.playmetric.repository.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.List;


@RestController
@RequestMapping("/api/events")
@Tag(name = "Event Controller", description = "APIs for game event tracking and analytics")
public class EventController {
    private final GameEventRepository gameEventRepository;
    private final LevelEventRepository levelEventRepository;
    private final EconomyEventRepository economyEventRepository;
    private final MissionEventRepository missionEventRepository;
    private final AdsEventRepository adsEventRepository;
    private final UIInteractionEventRepository uiInteractionEventRepository;

    public EventController(
        GameEventRepository gameEventRepository,
        LevelEventRepository levelEventRepository,
        EconomyEventRepository economyEventRepository,
        MissionEventRepository missionEventRepository,
        AdsEventRepository adsEventRepository,
        UIInteractionEventRepository uiInteractionEventRepository
    ) {
        this.gameEventRepository = gameEventRepository;
        this.levelEventRepository = levelEventRepository;
        this.economyEventRepository = economyEventRepository;
        this.missionEventRepository = missionEventRepository;
        this.adsEventRepository = adsEventRepository;
        this.uiInteractionEventRepository = uiInteractionEventRepository;
    }


    @PostMapping
    @Operation(summary = "Record a new event (generic)", description = "Use type-specific endpoints when possible. This generic endpoint will reject unknown payloads.")
    public ResponseEntity<?> recordEvent(@RequestBody java.util.Map<String, Object> payload) {
        // Generic endpoint: route by a simple `type` field if present
        var type = payload.getOrDefault("type", payload.get("eventType"));
        if (type == null) {
            return ResponseEntity.badRequest().body("Missing 'type' or 'eventType' in payload");
        }
        String t = type.toString().toLowerCase();
        try {
            switch (t) {
                case "game":
                case "game_start":
                case "gameevent":
                    var ge = new org.playmetric.model.GameEvent(
                        (String) payload.get("id"),
                        (String) payload.get("userId"),
                        mapToDeviceDetails((java.util.Map<String, Object>) payload.get("deviceDetails")),
                        payload.get("timestamp") == null ? java.time.Instant.now() : java.time.Instant.parse(payload.get("timestamp").toString()),
                        org.playmetric.model.EventType.valueOf(payload.getOrDefault("eventType", "GAME_START").toString()),
                        (String) payload.get("sessionId"),
                        (String) payload.get("playingPattern"),
                        payload.get("sessionDuration") == null ? 0L : Long.parseLong(payload.get("sessionDuration").toString())
                    );
                    return ResponseEntity.ok(gameEventRepository.save(ge));
                case "level":
                case "levelevent":
                    var le = new org.playmetric.model.LevelEvent(
                        (String) payload.get("id"),
                        (String) payload.get("userId"),
                        mapToDeviceDetails((java.util.Map<String, Object>) payload.get("deviceDetails")),
                        payload.get("timestamp") == null ? java.time.Instant.now() : java.time.Instant.parse(payload.get("timestamp").toString()),
                        org.playmetric.model.EventType.valueOf(payload.getOrDefault("eventType", "LEVEL_COMPLETE").toString()),
                        (String) payload.get("levelId"),
                        payload.get("attemptCount") == null ? 0 : Integer.parseInt(payload.get("attemptCount").toString()),
                        (String) payload.get("failReason"),
                        payload.get("levelDuration") == null ? 0L : Long.parseLong(payload.get("levelDuration").toString()),
                        payload.get("completed") == null ? false : Boolean.parseBoolean(payload.get("completed").toString())
                    );
                    return ResponseEntity.ok(levelEventRepository.save(le));
                default:
                    return ResponseEntity.badRequest().body("Unsupported event type: " + type);
            }
        } catch (Exception ex) {
            return ResponseEntity.status(500).body(ex.getMessage());
        }
    }

    private org.playmetric.model.DeviceDetails mapToDeviceDetails(java.util.Map<String, Object> m) {
        if (m == null) return null;
        // DeviceDetails record expects: deviceId, deviceModel, osVersion, platform, appVersion
        String deviceId = m.getOrDefault("deviceId", m.getOrDefault("id", null)) == null ? null : m.getOrDefault("deviceId", m.getOrDefault("id", null)).toString();
        String deviceModel = m.getOrDefault("deviceModel", m.getOrDefault("model", null)) == null ? null : m.getOrDefault("deviceModel", m.getOrDefault("model", null)).toString();
        String osVersion = m.getOrDefault("osVersion", m.getOrDefault("version", null)) == null ? null : m.getOrDefault("osVersion", m.getOrDefault("version", null)).toString();
        String platform = m.getOrDefault("os", null) == null ? null : m.get("os").toString();
        String appVersion = m.getOrDefault("appVersion", null) == null ? null : m.get("appVersion").toString();
        return new org.playmetric.model.DeviceDetails(deviceId, deviceModel, osVersion, platform, appVersion);
    }

    // Type-specific POST endpoints (preferred)
    @PostMapping("/game")
    public ResponseEntity<org.playmetric.model.GameEvent> postGameEvent(@RequestBody org.playmetric.model.GameEvent ge) {
        return ResponseEntity.ok(gameEventRepository.save(ge));
    }

    @PostMapping("/level")
    public ResponseEntity<org.playmetric.model.LevelEvent> postLevelEvent(@RequestBody org.playmetric.model.LevelEvent le) {
        return ResponseEntity.ok(levelEventRepository.save(le));
    }

    // Example: Get all game events for a user
    @GetMapping("/game/user/{userId}")

    public ResponseEntity<List<GameEvent>> getGameEventsByUser(@PathVariable String userId) {
        return ResponseEntity.ok(gameEventRepository.findAll().stream().filter(e -> e.userId().equals(userId)).toList());
    }

    // Example: Get all level events for a user
    @GetMapping("/level/user/{userId}")

    public ResponseEntity<List<LevelEvent>> getLevelEventsByUser(@PathVariable String userId) {
        return ResponseEntity.ok(levelEventRepository.findAll().stream().filter(e -> e.userId().equals(userId)).toList());
    }

    // Get all events grouped by type
    @GetMapping
    public ResponseEntity<java.util.Map<String, java.util.List<?>>> getAllEvents() {
        var map = new java.util.LinkedHashMap<String, java.util.List<?>>();
        map.put("game", gameEventRepository.findAll());
        map.put("level", levelEventRepository.findAll());
        map.put("economy", economyEventRepository.findAll());
        map.put("mission", missionEventRepository.findAll());
        map.put("ads", adsEventRepository.findAll());
        map.put("ui", uiInteractionEventRepository.findAll());
        return ResponseEntity.ok(map);
    }

    // Get events by type
    @GetMapping("/{type}")
    public ResponseEntity<?> getEventsByType(@PathVariable String type) {
        switch (type.toLowerCase()) {
            case "game":
                return ResponseEntity.ok(gameEventRepository.findAll());
            case "level":
                return ResponseEntity.ok(levelEventRepository.findAll());
            case "economy":
                return ResponseEntity.ok(economyEventRepository.findAll());
            case "mission":
                return ResponseEntity.ok(missionEventRepository.findAll());
            case "ads":
                return ResponseEntity.ok(adsEventRepository.findAll());
            case "ui":
                return ResponseEntity.ok(uiInteractionEventRepository.findAll());
            default:
                return ResponseEntity.badRequest().body("Unknown type: " + type);
        }
    }

    // Level-specific query: events for a given levelId
    @GetMapping("/level/id/{levelId}")
    public ResponseEntity<java.util.List<org.playmetric.model.LevelEvent>> getLevelEventsByLevelId(@PathVariable String levelId) {
        return ResponseEntity.ok(levelEventRepository.findAll().stream().filter(e -> levelId.equals(e.levelId())).toList());
    }

    // Game-specific query by user (already existed) and generic per-type by user
    @GetMapping("/{type}/user/{userId}")
    public ResponseEntity<?> getEventsByTypeAndUser(@PathVariable String type, @PathVariable String userId) {
        switch (type.toLowerCase()) {
            case "game":
                return ResponseEntity.ok(gameEventRepository.findAll().stream().filter(e -> userId.equals(e.userId())).toList());
            case "level":
                return ResponseEntity.ok(levelEventRepository.findAll().stream().filter(e -> userId.equals(e.userId())).toList());
            case "economy":
                return ResponseEntity.ok(economyEventRepository.findAll().stream().filter(e -> userId.equals(e.userId())).toList());
            case "mission":
                return ResponseEntity.ok(missionEventRepository.findAll().stream().filter(e -> userId.equals(e.userId())).toList());
            case "ads":
                return ResponseEntity.ok(adsEventRepository.findAll().stream().filter(e -> userId.equals(e.userId())).toList());
            case "ui":
                return ResponseEntity.ok(uiInteractionEventRepository.findAll().stream().filter(e -> userId.equals(e.userId())).toList());
            default:
                return ResponseEntity.badRequest().body("Unknown type: " + type);
        }
    }

    // Add similar endpoints for other event types as needed
}
