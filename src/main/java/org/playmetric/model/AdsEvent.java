
package org.playmetric.model;

public record AdsEvent(
    String id,
    String userId,
    DeviceDetails deviceDetails,
    java.time.Instant timestamp,
    EventType eventType,
    String adEventType,
    double revenue,
    String adId
) {}
