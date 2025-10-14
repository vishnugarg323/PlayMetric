
package org.playmetric.model;

import java.time.Instant;

public record BaseEvent(
    String id,
    String userId,
    DeviceDetails deviceDetails,
    Instant timestamp,
    EventType eventType
) {}
