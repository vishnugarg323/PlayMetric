package org.playmetric.model;

import io.swagger.v3.oas.annotations.media.Schema;

import java.time.Instant;

/**
 * Global event parameters that are common to all event types.
 * These parameters provide essential context for every event and enable
 * comprehensive user tracking, session management, and device analytics.
 * 
 * <p>This data is crucial for AI-driven analytics including:
 * <ul>
 *   <li>User behavior analysis and churn prediction</li>
 *   <li>Session-based engagement metrics</li>
 *   <li>Device and platform performance analysis</li>
 *   <li>Cross-session user journey tracking</li>
 * </ul>
 * 
 * @param userId Unique identifier for the user across all sessions and devices
 * @param deviceId Unique identifier for the device (useful for multi-device tracking)
 * @param deviceModel Model of the device (e.g., "iPhone 14 Pro", "Samsung Galaxy S23")
 * @param osVersion Operating system version (e.g., "iOS 17.1", "Android 14")
 * @param platform Platform identifier (e.g., "iOS", "Android", "Windows", "WebGL")
 * @param appVersion Version of the game/app (e.g., "1.2.3")
 * @param timestamp UTC timestamp when the event occurred
 * @param sessionId Unique identifier for the current play session
 * @param sessionDuration Duration of the current session in milliseconds (0 for session start events)
 */
@Schema(description = "Global parameters shared across all event types, providing user, device, and session context")
public record GlobalEventParameters(
    @Schema(description = "Unique identifier for the user", example = "user_12345")
    String userId,
    
    @Schema(description = "Unique identifier for the device", example = "device_abc123")
    String deviceId,
    
    @Schema(description = "Model of the device", example = "iPhone 14 Pro")
    String deviceModel,
    
    @Schema(description = "Operating system version", example = "iOS 17.1")
    String osVersion,
    
    @Schema(description = "Platform identifier", example = "iOS")
    String platform,
    
    @Schema(description = "Version of the game/app", example = "1.2.3")
    String appVersion,
    
    @Schema(description = "UTC timestamp when the event occurred", example = "2025-10-14T12:00:00Z")
    Instant timestamp,
    
    @Schema(description = "Unique identifier for the current play session", example = "session_xyz789")
    String sessionId,
    
    @Schema(description = "Duration of the current session in milliseconds", example = "1800000")
    Long sessionDuration
) {
    /**
     * Creates GlobalEventParameters with current timestamp if not provided.
     * This constructor allows automatic timestamp generation for convenience.
     */
    public GlobalEventParameters {
        if (timestamp == null) {
            timestamp = Instant.now();
        }
        if (sessionDuration == null) {
            sessionDuration = 0L;
        }
    }
}
