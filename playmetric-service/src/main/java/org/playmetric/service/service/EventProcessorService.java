package org.playmetric.service.service;

import lombok.RequiredArgsConstructor;
import org.playmetric.service.model.BaseEvent;
import org.playmetric.service.model.EventType;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class EventProcessorService {
    private final MongoTemplate eventMongoTemplate;
    private final MongoTemplate analyticsMongoTemplate;

    @Async
    public void processEvent(BaseEvent event) {
        // Store in main event collection
        eventMongoTemplate.save(event);

        // Process for analytics based on event type
        switch (event.getEventType()) {
            case LEVEL_START, LEVEL_END, LEVEL_FAILED ->
                processLevelAnalytics(event);
            case GAME_START, GAME_END ->
                processGameAnalytics(event);
            case ECONOMY_TRANSACTION ->
                processEconomyAnalytics(event);
            case AD_SHOWN, AD_COMPLETED ->
                processAdAnalytics(event);
        }
    }

    private void processLevelAnalytics(BaseEvent event) {
        analyticsMongoTemplate.save(event, "level_analytics");
    }

    private void processGameAnalytics(BaseEvent event) {
        analyticsMongoTemplate.save(event, "game_session_analytics");
    }

    private void processEconomyAnalytics(BaseEvent event) {
        analyticsMongoTemplate.save(event, "economy_analytics");
    }

    private void processAdAnalytics(BaseEvent event) {
        analyticsMongoTemplate.save(event, "ad_analytics");
    }
}
