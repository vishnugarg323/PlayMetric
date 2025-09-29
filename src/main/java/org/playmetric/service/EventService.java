package org.playmetric.service;

import lombok.RequiredArgsConstructor;
import org.playmetric.model.BaseEvent;
import org.playmetric.repository.EventRepository;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;

@Service
@RequiredArgsConstructor
public class EventService {
    private final EventRepository eventRepository;

    public BaseEvent saveEvent(BaseEvent event) {
        if (event.getTimestamp() == null) {
            event.setTimestamp(Instant.now());
        }
        return eventRepository.save(event);
    }

    public List<BaseEvent> getEventsByUserAndTimeRange(String userId, Instant start, Instant end) {
        return eventRepository.findByUserIdAndTimestampBetween(userId, start, end);
    }

    public List<BaseEvent> getEventsByType(String eventType) {
        return eventRepository.findByEventType(eventType);
    }
}
