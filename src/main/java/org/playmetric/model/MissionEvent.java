
package org.playmetric.model;

public record MissionEvent(
    String id,
    String userId,
    DeviceDetails deviceDetails,
    java.time.Instant timestamp,
    EventType eventType,
    String missionType,
    String missionId,
    boolean completed,
    long missionDuration
) {}
