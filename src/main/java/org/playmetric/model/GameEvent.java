
package org.playmetric.model;

import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Represents a game-level event such as game start, end, or session-related events.
 * Each event is linked to a user and contains comprehensive metrics for AI analysis.
 * 
 * <p>Key metrics for AI analysis:
 * <ul>
 *   <li>Session duration and patterns for engagement analysis</li>
 *   <li>Score progression for difficulty assessment</li>
 *   <li>Lives and health tracking for balance analysis</li>
 *   <li>Power-up usage for monetization insights</li>
 *   <li>Enemy/boss defeats for content completion tracking</li>
 * </ul>
 * 
 * @param id Auto-generated unique identifier for this event (MongoDB ObjectId)
 * @param globalParams Common parameters shared across all events
 * @param eventType Specific type of game event (SESSION_START, GAME_END, etc.)
 * @param gameId Identifier for the specific game or game mode
 * @param score Current score at the time of the event
 * @param highScore Player's high score at the time of the event
 * @param livesRemaining Number of lives remaining
 * @param healthRemaining Current health value
 * @param powerupsUsed Number of power-ups used in this session
 * @param enemiesDefeated Number of enemies defeated in this session
 * @param bossesDefeated Number of bosses defeated in this session
 * @param playingPattern Pattern of play (e.g., "aggressive", "defensive", "explorer")
 * @param additionalData Any additional custom data in JSON format
 */
@Document(collection = "game_events")
@Schema(description = "Game session and gameplay events with comprehensive metrics")
public record GameEvent(
    @Id
    @Schema(description = "Auto-generated unique identifier", example = "507f1f77bcf86cd799439011")
    String id,
    
    @Schema(description = "Global event parameters common to all events")
    GlobalEventParameters globalParams,
    
    @Schema(description = "Type of game event", example = "SESSION_START")
    EventType eventType,
    
    @Schema(description = "Identifier for the game or game mode", example = "adventure_mode_1")
    String gameId,
    
    @Schema(description = "Current score", example = "1500")
    Long score,
    
    @Schema(description = "Player's high score", example = "5000")
    Long highScore,
    
    @Schema(description = "Number of lives remaining", example = "3")
    Integer livesRemaining,
    
    @Schema(description = "Current health value", example = "75")
    Integer healthRemaining,
    
    @Schema(description = "Number of power-ups used", example = "2")
    Integer powerupsUsed,
    
    @Schema(description = "Number of enemies defeated", example = "45")
    Integer enemiesDefeated,
    
    @Schema(description = "Number of bosses defeated", example = "1")
    Integer bossesDefeated,
    
    @Schema(description = "Playing pattern or style", example = "aggressive")
    String playingPattern,
    
    @Schema(description = "Additional custom data in JSON format", example = "{\"weapon\": \"sword\", \"difficulty\": \"hard\"}")
    String additionalData
) {
    /**
     * Creates a GameEvent with null checks for optional fields.
     */
    public GameEvent {
        // Ensure globalParams is not null
        if (globalParams == null) {
            throw new IllegalArgumentException("globalParams cannot be null");
        }
    }
}
