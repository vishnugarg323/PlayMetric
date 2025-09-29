package org.playmetric.model;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;

@Data
@Document(collection = "events")
public class BaseEvent {
    @Id
    private String id;
    private String userId;
    private DeviceDetails deviceDetails;
    private Instant timestamp;
    private EventType eventType;
}
