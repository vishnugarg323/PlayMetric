
package org.playmetric.model;

public record UIInteractionEvent(
    String id,
    String userId,
    DeviceDetails deviceDetails,
    java.time.Instant timestamp,
    EventType eventType,
    String interactionType,
    String details
) {}
