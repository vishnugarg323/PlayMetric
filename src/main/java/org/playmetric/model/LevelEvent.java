package org.playmetric.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class LevelEvent extends BaseEvent {
    private String levelId;
    private int attemptCount;
    private String failReason;
    private long levelDuration;
    private boolean completed;
}
