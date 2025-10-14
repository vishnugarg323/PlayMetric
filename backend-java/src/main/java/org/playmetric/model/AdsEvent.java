
package org.playmetric.model;

import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Represents an advertisement event such as ad loaded, shown, completed, or clicked.
 * Essential for ad monetization analysis and user experience optimization.
 * 
 * <p>Key metrics for AI analysis:
 * <ul>
 *   <li>Ad completion rates for engagement analysis</li>
 *   <li>Revenue per user for monetization optimization</li>
 *   <li>Ad placement effectiveness</li>
 *   <li>User tolerance and skip patterns</li>
 * </ul>
 */
@Document(collection = "ads_events")
@Schema(description = "Advertisement events with revenue and engagement tracking")
public record AdsEvent(
    @Id
    @Schema(description = "Auto-generated unique identifier", example = "507f1f77bcf86cd799439011")
    String id,
    
    @Schema(description = "Global event parameters common to all events")
    GlobalEventParameters globalParams,
    
    @Schema(description = "Type of ad event", example = "AD_COMPLETED")
    EventType eventType,
    
    @Schema(description = "Specific ad event type", example = "rewarded")
    String adEventType,
    
    @Schema(description = "Revenue generated from ad", example = "0.05")
    Double revenue,
    
    @Schema(description = "Unique ad identifier", example = "ad_xyz123")
    String adId,
    
    @Schema(description = "Ad network/provider", example = "admob")
    String adNetwork,
    
    @Schema(description = "Ad placement location", example = "level_complete_screen")
    String adPlacement,
    
    @Schema(description = "Ad format", example = "video")
    String adFormat,
    
    @Schema(description = "Duration ad was shown (milliseconds)", example = "30000")
    Long adDuration,
    
    @Schema(description = "Whether ad was skipped", example = "false")
    Boolean skipped,
    
    @Schema(description = "Whether ad was clicked", example = "false")
    Boolean clicked,
    
    @Schema(description = "Reward type if rewarded ad", example = "extra_life")
    String rewardType,
    
    @Schema(description = "Reward amount if rewarded ad", example = "1")
    Double rewardAmount,
    
    @Schema(description = "Additional custom data", example = "{\"advertiser\": \"brand_x\"}")
    String additionalData
) {
    public AdsEvent {
        if (globalParams == null) {
            throw new IllegalArgumentException("globalParams cannot be null");
        }
    }
}
