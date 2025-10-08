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
    @Operation(summary = "Record a new game event", description = "Accepts and stores various types of game events")
    public ResponseEntity<?> recordEvent(@RequestBody Object event) {
        if (event instanceof GameEvent ge) {
            return ResponseEntity.ok(gameEventRepository.save(ge));
        } else if (event instanceof LevelEvent le) {
            return ResponseEntity.ok(levelEventRepository.save(le));
        } else if (event instanceof EconomyEvent ee) {
            return ResponseEntity.ok(economyEventRepository.save(ee));
        } else if (event instanceof MissionEvent me) {
            return ResponseEntity.ok(missionEventRepository.save(me));
        } else if (event instanceof AdsEvent ae) {
            return ResponseEntity.ok(adsEventRepository.save(ae));
        } else if (event instanceof UIInteractionEvent ue) {
            return ResponseEntity.ok(uiInteractionEventRepository.save(ue));
        } else {
            return ResponseEntity.badRequest().body("Unknown event type");
        }
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

    // Add similar endpoints for other event types as needed
}
