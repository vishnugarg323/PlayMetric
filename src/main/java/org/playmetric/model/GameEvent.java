
package org.playmetric.model;

public record GameEvent(
    String id,
    String userId,
    DeviceDetails deviceDetails,
    java.time.Instant timestamp,
    EventType eventType,
    String sessionId,
    String playingPattern,
    long sessionDuration
) {}
