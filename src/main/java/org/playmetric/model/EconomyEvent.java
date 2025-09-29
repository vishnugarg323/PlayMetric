package org.playmetric.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class EconomyEvent extends BaseEvent {
    private String transactionId;
    private String currencyType;
    private double amount;
    private String transactionType; // PURCHASE, SELL, REWARD
    private double realMoneyValue;
}
