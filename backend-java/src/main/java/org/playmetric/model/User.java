package org.playmetric.model;

import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;

/**
 * Represents a game user with their profile information and activity metrics.
 * This entity is automatically created when a user first sends an event and
 * is updated with each subsequent interaction.
 * 
 * <p>Essential for AI-driven analytics:
 * <ul>
 *   <li>User retention and churn prediction</li>
 *   <li>Lifetime value (LTV) calculation</li>
 *   <li>User segmentation and cohort analysis</li>
 *   <li>Device and platform preference analysis</li>
 *   <li>Cross-device user identification</li>
 * </ul>
 */
@Document(collection = "users")
@Schema(description = "User profile with activity tracking and device information")
public class User {
    
    @Id
    @Schema(description = "Unique identifier for the user", example = "user_12345")
    private String userId;
    
    @Schema(description = "User's primary device ID", example = "device_abc123")
    private String deviceId;
    
    @Schema(description = "User's device model", example = "iPhone 14 Pro")
    private String deviceModel;
    
    @Schema(description = "User's operating system version", example = "iOS 17.1")
    private String osVersion;
    
    @Schema(description = "User's platform", example = "iOS")
    private String platform;
    
    @Schema(description = "User's app version", example = "1.2.3")
    private String appVersion;
    
    @Schema(description = "Timestamp when user was first seen", example = "2025-10-14T12:00:00Z")
    private Instant firstSeen;
    
    @Schema(description = "Timestamp when user was last seen", example = "2025-10-14T18:30:00Z")
    private Instant lastSeen;
    
    @Schema(description = "Total number of events recorded for this user", example = "245")
    private long totalEvents;
    
    @Schema(description = "Total number of sessions for this user", example = "42")
    private long totalSessions;
    
    @Schema(description = "User's current session ID", example = "session_xyz789")
    private String currentSessionId;

    // Constructors
    public User() {
    }

    public User(String userId, String deviceId, String deviceModel, String osVersion, 
                String platform, String appVersion, Instant firstSeen, Instant lastSeen,
                long totalEvents, long totalSessions, String currentSessionId) {
        this.userId = userId;
        this.deviceId = deviceId;
        this.deviceModel = deviceModel;
        this.osVersion = osVersion;
        this.platform = platform;
        this.appVersion = appVersion;
        this.firstSeen = firstSeen;
        this.lastSeen = lastSeen;
        this.totalEvents = totalEvents;
        this.totalSessions = totalSessions;
        this.currentSessionId = currentSessionId;
    }

    /**
     * Creates a new User from GlobalEventParameters.
     * Sets firstSeen and lastSeen to current timestamp.
     */
    public static User fromGlobalParams(GlobalEventParameters params) {
        Instant now = params.timestamp() != null ? params.timestamp() : Instant.now();
        return new User(
            params.userId(),
            params.deviceId(),
            params.deviceModel(),
            params.osVersion(),
            params.platform(),
            params.appVersion(),
            now,
            now,
            0L,
            0L,
            params.sessionId()
        );
    }

    /**
     * Updates user information from GlobalEventParameters.
     * Increments event count and updates lastSeen timestamp.
     */
    public void updateFromGlobalParams(GlobalEventParameters params) {
        this.lastSeen = params.timestamp() != null ? params.timestamp() : Instant.now();
        this.totalEvents++;
        
        // Update device info if changed (user might switch devices)
        if (params.deviceId() != null && !params.deviceId().equals(this.deviceId)) {
            this.deviceId = params.deviceId();
            this.deviceModel = params.deviceModel();
            this.osVersion = params.osVersion();
            this.platform = params.platform();
        }
        
        // Update app version if changed
        if (params.appVersion() != null && !params.appVersion().equals(this.appVersion)) {
            this.appVersion = params.appVersion();
        }
        
        // Track new session
        if (params.sessionId() != null && !params.sessionId().equals(this.currentSessionId)) {
            this.currentSessionId = params.sessionId();
            this.totalSessions++;
        }
    }

    // Getters and Setters
    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public void setDeviceId(String deviceId) {
        this.deviceId = deviceId;
    }

    public String getDeviceModel() {
        return deviceModel;
    }

    public void setDeviceModel(String deviceModel) {
        this.deviceModel = deviceModel;
    }

    public String getOsVersion() {
        return osVersion;
    }

    public void setOsVersion(String osVersion) {
        this.osVersion = osVersion;
    }

    public String getPlatform() {
        return platform;
    }

    public void setPlatform(String platform) {
        this.platform = platform;
    }

    public String getAppVersion() {
        return appVersion;
    }

    public void setAppVersion(String appVersion) {
        this.appVersion = appVersion;
    }

    public Instant getFirstSeen() {
        return firstSeen;
    }

    public void setFirstSeen(Instant firstSeen) {
        this.firstSeen = firstSeen;
    }

    public Instant getLastSeen() {
        return lastSeen;
    }

    public void setLastSeen(Instant lastSeen) {
        this.lastSeen = lastSeen;
    }

    public long getTotalEvents() {
        return totalEvents;
    }

    public void setTotalEvents(long totalEvents) {
        this.totalEvents = totalEvents;
    }

    public long getTotalSessions() {
        return totalSessions;
    }

    public void setTotalSessions(long totalSessions) {
        this.totalSessions = totalSessions;
    }

    public String getCurrentSessionId() {
        return currentSessionId;
    }

    public void setCurrentSessionId(String currentSessionId) {
        this.currentSessionId = currentSessionId;
    }
}
