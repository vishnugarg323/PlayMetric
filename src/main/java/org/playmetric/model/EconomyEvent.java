
package org.playmetric.model;

public record EconomyEvent(
    String id,
    String userId,
    DeviceDetails deviceDetails,
    java.time.Instant timestamp,
    EventType eventType,
    String transactionId,
    String currencyType,
    double amount,
    String transactionType,
    double realMoneyValue
) {}
