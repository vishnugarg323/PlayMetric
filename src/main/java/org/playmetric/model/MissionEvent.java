
package org.playmetric.model;

import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Represents a mission/quest event in the game.
 * Missions provide structured objectives and are key for engagement tracking.
 * 
 * <p>Key metrics for AI analysis:
 * <ul>
 *   <li>Mission completion rates for difficulty assessment</li>
 *   <li>Time-to-complete for pacing analysis</li>
 *   <li>Abandonment patterns for content optimization</li>
 *   <li>Reward effectiveness for motivation analysis</li>
 * </ul>
 */
@Document(collection = "mission_events")
@Schema(description = "Mission and quest events with completion tracking")
public record MissionEvent(
    @Id
    @Schema(description = "Auto-generated unique identifier", example = "507f1f77bcf86cd799439011")
    String id,
    
    @Schema(description = "Global event parameters common to all events")
    GlobalEventParameters globalParams,
    
    @Schema(description = "Type of mission event", example = "MISSION_COMPLETE")
    EventType eventType,
    
    @Schema(description = "Type/category of mission", example = "daily_challenge")
    String missionType,
    
    @Schema(description = "Unique mission identifier", example = "mission_daily_001")
    String missionId,
    
    @Schema(description = "Mission name", example = "Defeat 10 Enemies")
    String missionName,
    
    @Schema(description = "Whether mission was completed", example = "true")
    Boolean completed,
    
    @Schema(description = "Time spent on mission (milliseconds)", example = "300000")
    Long missionDuration,
    
    @Schema(description = "Progress percentage", example = "75")
    Integer progressPercentage,
    
    @Schema(description = "Number of attempts", example = "2")
    Integer attemptCount,
    
    @Schema(description = "Reward type", example = "gold_coins")
    String rewardType,
    
    @Schema(description = "Reward amount", example = "500")
    Double rewardAmount,
    
    @Schema(description = "Whether reward was claimed", example = "true")
    Boolean rewardClaimed,
    
    @Schema(description = "Additional custom data", example = "{\"difficulty\": \"hard\"}")
    String additionalData
) {
    public MissionEvent {
        if (globalParams == null) {
            throw new IllegalArgumentException("globalParams cannot be null");
        }
    }
}
