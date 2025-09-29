package org.playmetric.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class GameEvent extends BaseEvent {
    private String sessionId;
    private String playingPattern;
    private long sessionDuration;
}
