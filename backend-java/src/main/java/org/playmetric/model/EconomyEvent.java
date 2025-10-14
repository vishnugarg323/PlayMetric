
package org.playmetric.model;

import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Represents an in-game economy event such as purchases, currency transactions, and rewards.
 * Critical for monetization analysis and economy balancing.
 * 
 * <p>Key metrics for AI analysis:
 * <ul>
 *   <li>Transaction patterns for monetization optimization</li>
 *   <li>Currency flow analysis for economy balancing</li>
 *   <li>IAP conversion and revenue tracking</li>
 *   <li>Item popularity and pricing effectiveness</li>
 * </ul>
 */
@Document(collection = "economy_events")
@Schema(description = "In-game economy events including purchases and transactions")
public record EconomyEvent(
    @Id
    @Schema(description = "Auto-generated unique identifier", example = "507f1f77bcf86cd799439011")
    String id,
    
    @Schema(description = "Global event parameters common to all events")
    GlobalEventParameters globalParams,
    
    @Schema(description = "Type of economy event", example = "ECONOMY_CURRENCY_PURCHASE")
    EventType eventType,
    
    @Schema(description = "Unique transaction identifier", example = "txn_abc123")
    String transactionId,
    
    @Schema(description = "Type of currency or item", example = "gold_coins")
    String currencyType,
    
    @Schema(description = "Amount of currency/items", example = "1000")
    Double amount,
    
    @Schema(description = "Type of transaction", example = "purchase")
    String transactionType,
    
    @Schema(description = "Real money value in USD", example = "4.99")
    Double realMoneyValue,
    
    @Schema(description = "Item ID if applicable", example = "item_sword_legendary")
    String itemId,
    
    @Schema(description = "Item name", example = "Legendary Sword")
    String itemName,
    
    @Schema(description = "Item category", example = "weapon")
    String itemCategory,
    
    @Schema(description = "Balance before transaction", example = "500")
    Double balanceBefore,
    
    @Schema(description = "Balance after transaction", example = "1500")
    Double balanceAfter,
    
    @Schema(description = "Source of currency/item", example = "level_reward")
    String source,
    
    @Schema(description = "Additional custom data", example = "{\"promo_code\": \"SAVE20\"}")
    String additionalData
) {
    public EconomyEvent {
        if (globalParams == null) {
            throw new IllegalArgumentException("globalParams cannot be null");
        }
    }
}
