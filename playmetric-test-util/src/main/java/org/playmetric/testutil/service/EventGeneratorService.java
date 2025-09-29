package org.playmetric.testutil.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.playmetric.testutil.config.EventGeneratorConfig;
import org.playmetric.testutil.model.BaseEvent;
import org.playmetric.testutil.model.EventType;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;

@Slf4j
@Service
@RequiredArgsConstructor
public class EventGeneratorService {
    private final RestTemplate restTemplate;
    private final EventGeneratorConfig config;
    private final Random random = new Random();
    private final AtomicInteger eventCount = new AtomicInteger(0);

    @Scheduled(fixedDelayString = "${event.generator.target.delay-between-batches-ms}")
    public void generateAndSendEvents() {
        if (eventCount.get() >= config.getTotalEvents()) {
            log.info("Completed generating {} events", config.getTotalEvents());
            return;
        }

        int batchSize = Math.min(
            config.getBatchSize(),
            config.getTotalEvents() - eventCount.get()
        );

        for (int i = 0; i < batchSize; i++) {
            try {
                BaseEvent event = generateRandomEvent();
                sendEvent(event);
                eventCount.incrementAndGet();
            } catch (Exception e) {
                log.error("Failed to send event: {}", e.getMessage());
            }
        }
    }

    private BaseEvent generateRandomEvent() {
        EventType[] types = EventType.values();
        EventType randomType = types[random.nextInt(types.length)];

        BaseEvent event = new BaseEvent();
        event.setEventType(randomType);
        // Set other event properties based on type
        // This will be expanded based on event types
        return event;
    }

    private void sendEvent(BaseEvent event) {
        try {
            restTemplate.postForObject(config.getTargetUrl(), event, BaseEvent.class);
            log.debug("Sent event: {}", event);
        } catch (Exception e) {
            log.error("Failed to send event: {}", e.getMessage());
            throw e;
        }
    }
}
