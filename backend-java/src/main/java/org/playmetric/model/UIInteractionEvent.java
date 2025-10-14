
package org.playmetric.model;

import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Represents a user interface interaction event.
 * Tracks how users interact with menus, buttons, and UI elements.
 * 
 * <p>Key metrics for AI analysis:
 * <ul>
 *   <li>UI navigation patterns for UX optimization</li>
 *   <li>Feature discovery and usage analysis</li>
 *   <li>Bottleneck identification in user flows</li>
 *   <li>A/B testing for UI improvements</li>
 * </ul>
 */
@Document(collection = "ui_interaction_events")
@Schema(description = "User interface interaction events for UX analysis")
public record UIInteractionEvent(
    @Id
    @Schema(description = "Auto-generated unique identifier", example = "507f1f77bcf86cd799439011")
    String id,
    
    @Schema(description = "Global event parameters common to all events")
    GlobalEventParameters globalParams,
    
    @Schema(description = "Type of UI event", example = "UI_BUTTON_CLICK")
    EventType eventType,
    
    @Schema(description = "Type of interaction", example = "button_click")
    String interactionType,
    
    @Schema(description = "Screen or view name", example = "main_menu")
    String screenName,
    
    @Schema(description = "UI element identifier", example = "btn_play_now")
    String elementId,
    
    @Schema(description = "UI element name", example = "Play Now Button")
    String elementName,
    
    @Schema(description = "UI element type", example = "button")
    String elementType,
    
    @Schema(description = "Previous screen", example = "splash_screen")
    String previousScreen,
    
    @Schema(description = "Additional interaction details", example = "Navigated to level selection")
    String details,
    
    @Schema(description = "Additional custom data", example = "{\"button_color\": \"blue\"}")
    String additionalData
) {
    public UIInteractionEvent {
        if (globalParams == null) {
            throw new IllegalArgumentException("globalParams cannot be null");
        }
    }
}
