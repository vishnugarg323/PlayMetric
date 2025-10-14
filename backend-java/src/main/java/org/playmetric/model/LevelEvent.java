
package org.playmetric.model;

import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Represents a level-specific event such as level start, complete, or fail.
 * Level events are critical for AI-driven level difficulty analysis and player progression tracking.
 * 
 * <p>Key metrics for AI analysis:
 * <ul>
 *   <li>Attempt count and completion rate for difficulty calibration</li>
 *   <li>Duration and time-to-complete for pacing analysis</li>
 *   <li>Fail reasons for identifying problematic game mechanics</li>
 *   <li>Star rating and perfect completion for skill assessment</li>
 *   <li>Resource usage and collection for economy balancing</li>
 *   <li>Hints and skips usage for accessibility insights</li>
 * </ul>
 * 
 * @param id Auto-generated unique identifier for this event (MongoDB ObjectId)
 * @param globalParams Common parameters shared across all events
 * @param eventType Specific type of level event (LEVEL_START, LEVEL_COMPLETE, LEVEL_FAIL, etc.)
 * @param gameId Identifier for the game this level belongs to (links to GameEvent)
 * @param levelId Unique identifier for the level
 * @param levelNumber Sequential level number in the game
 * @param difficulty Difficulty rating of the level (e.g., "easy", "medium", "hard")
 * @param attemptCount Number of times user has attempted this level
 * @param completed Whether the level was completed successfully
 * @param levelDuration Time spent in the level (milliseconds)
 * @param score Score achieved in this level
 * @param starsEarned Number of stars earned (typically 0-3)
 * @param perfectCompletion Whether the level was completed perfectly (no damage, all collectibles, etc.)
 * @param failReason Reason for failure (if applicable)
 * @param checkpointReached Last checkpoint reached in the level
 * @param hintsUsed Number of hints used
 * @param skipsUsed Number of skips used
 * @param itemsCollected Number of items collected in the level
 * @param enemiesDefeated Number of enemies defeated in the level
 * @param damagesTaken Number of times player took damage
 * @param powerupsUsed Number of power-ups used in the level
 * @param additionalData Any additional custom data in JSON format
 */
@Document(collection = "level_events")
@Schema(description = "Level progression events with detailed performance metrics")
public record LevelEvent(
    @Id
    @Schema(description = "Auto-generated unique identifier", example = "507f1f77bcf86cd799439011")
    String id,
    
    @Schema(description = "Global event parameters common to all events")
    GlobalEventParameters globalParams,
    
    @Schema(description = "Type of level event", example = "LEVEL_COMPLETE")
    EventType eventType,
    
    @Schema(description = "Identifier for the game this level belongs to", example = "adventure_mode_1")
    String gameId,
    
    @Schema(description = "Unique identifier for the level", example = "level_1_1")
    String levelId,
    
    @Schema(description = "Sequential level number", example = "1")
    Integer levelNumber,
    
    @Schema(description = "Difficulty rating", example = "medium")
    String difficulty,
    
    @Schema(description = "Number of attempts on this level", example = "3")
    Integer attemptCount,
    
    @Schema(description = "Whether the level was completed", example = "true")
    Boolean completed,
    
    @Schema(description = "Time spent in the level (milliseconds)", example = "180000")
    Long levelDuration,
    
    @Schema(description = "Score achieved", example = "950")
    Long score,
    
    @Schema(description = "Number of stars earned (0-3)", example = "2")
    Integer starsEarned,
    
    @Schema(description = "Perfect completion flag", example = "false")
    Boolean perfectCompletion,
    
    @Schema(description = "Reason for failure", example = "ran_out_of_time")
    String failReason,
    
    @Schema(description = "Last checkpoint reached", example = "checkpoint_3")
    String checkpointReached,
    
    @Schema(description = "Number of hints used", example = "1")
    Integer hintsUsed,
    
    @Schema(description = "Number of skips used", example = "0")
    Integer skipsUsed,
    
    @Schema(description = "Number of items collected", example = "15")
    Integer itemsCollected,
    
    @Schema(description = "Number of enemies defeated", example = "8")
    Integer enemiesDefeated,
    
    @Schema(description = "Number of damages taken", example = "5")
    Integer damagesTaken,
    
    @Schema(description = "Number of power-ups used", example = "2")
    Integer powerupsUsed,
    
    @Schema(description = "Additional custom data in JSON format", example = "{\"path_taken\": \"shortcut\", \"secrets_found\": 2}")
    String additionalData
) {
    /**
     * Creates a LevelEvent with null checks for required fields.
     */
    public LevelEvent {
        // Ensure required fields are not null
        if (globalParams == null) {
            throw new IllegalArgumentException("globalParams cannot be null");
        }
        if (levelId == null || levelId.trim().isEmpty()) {
            throw new IllegalArgumentException("levelId cannot be null or empty");
        }
    }
}
