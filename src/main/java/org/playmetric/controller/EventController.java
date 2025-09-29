package org.playmetric.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.playmetric.model.BaseEvent;
import org.playmetric.service.EventService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.List;

@RestController
@RequestMapping("/api/events")
@RequiredArgsConstructor
@Tag(name = "Event Controller", description = "APIs for game event tracking and analytics")
public class EventController {
    private final EventService eventService;

    @PostMapping
    @Operation(summary = "Record a new game event", description = "Accepts and stores various types of game events")
    public ResponseEntity<BaseEvent> recordEvent(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(description = "Event details to be recorded")
            @RequestBody BaseEvent event) {
        return ResponseEntity.ok(eventService.saveEvent(event));
    }

    @GetMapping("/user/{userId}")
    @Operation(summary = "Get user events", description = "Retrieve events for a specific user within a time range")
    public ResponseEntity<List<BaseEvent>> getUserEvents(
            @Parameter(description = "ID of the user") @PathVariable String userId,
            @Parameter(description = "Start time for event query") @RequestParam Instant startTime,
            @Parameter(description = "End time for event query") @RequestParam Instant endTime) {
        return ResponseEntity.ok(eventService.getEventsByUserAndTimeRange(userId, startTime, endTime));
    }

    @GetMapping("/type/{eventType}")
    @Operation(summary = "Get events by type", description = "Retrieve all events of a specific type")
    public ResponseEntity<List<BaseEvent>> getEventsByType(
            @Parameter(description = "Type of event to query") @PathVariable String eventType) {
        return ResponseEntity.ok(eventService.getEventsByType(eventType));
    }
}
