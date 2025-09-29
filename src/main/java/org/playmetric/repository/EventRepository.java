package org.playmetric.repository;

import org.playmetric.model.BaseEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;

@Repository
public interface EventRepository extends MongoRepository<BaseEvent, String> {
    List<BaseEvent> findByUserIdAndTimestampBetween(String userId, Instant start, Instant end);
    List<BaseEvent> findByEventType(String eventType);
}
