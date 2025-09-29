package org.playmetric.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.playmetric.model.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.time.Instant;
import java.util.*;

@Slf4j
@Component
public class GameEventGenerator {
    private static final String[] USER_IDS = {"user1", "user2", "user3", "user4", "user5"};
    private static final String[] DEVICE_MODELS = {"iPhone 13", "Samsung S21", "Pixel 6", "OnePlus 9", "iPad Pro"};
    private static final String[] PLATFORMS = {"iOS", "Android", "Web"};
    private static final String[] LEVEL_IDS = {"level_1", "level_2", "level_3", "level_4", "level_5"};
    private static final String[] CURRENCIES = {"gold", "gems", "coins"};

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final Random random = new Random();

    public void generateAndSaveEvents(String filePath, int count, EventType eventType) throws IOException {
        List<BaseEvent> events = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            events.add(createEvent(eventType));
        }
        objectMapper.writerWithDefaultPrettyPrinter().writeValue(new File(filePath), events);
    }

    private BaseEvent createEvent(EventType eventType) {
        switch (eventType) {
            case GAME_START, GAME_END -> {
                GameEvent event = new GameEvent();
                populateBaseFields(event, eventType);
                event.setSessionId(UUID.randomUUID().toString());
                event.setPlayingPattern("pattern_" + random.nextInt(5));
                event.setSessionDuration(random.nextInt(3600));
                return event;
            }
            case LEVEL_START, LEVEL_END, LEVEL_FAILED -> {
                LevelEvent event = new LevelEvent();
                populateBaseFields(event, eventType);
                event.setLevelId(LEVEL_IDS[random.nextInt(LEVEL_IDS.length)]);
                event.setAttemptCount(random.nextInt(5) + 1);
                if (eventType == EventType.LEVEL_FAILED) {
                    event.setFailReason("reason_" + random.nextInt(3));
                }
                event.setLevelDuration(random.nextInt(600));
                event.setCompleted(eventType == EventType.LEVEL_END);
                return event;
            }
            case ECONOMY_TRANSACTION -> {
                EconomyEvent event = new EconomyEvent();
                populateBaseFields(event, eventType);
                event.setTransactionId(UUID.randomUUID().toString());
                event.setCurrencyType(CURRENCIES[random.nextInt(CURRENCIES.length)]);
                event.setAmount(random.nextDouble() * 1000);
                event.setTransactionType(random.nextBoolean() ? "PURCHASE" : "SELL");
                event.setRealMoneyValue(random.nextDouble() * 100);
                return event;
            }
            default -> {
                BaseEvent event = new BaseEvent();
                populateBaseFields(event, eventType);
                return event;
            }
        }
    }

    private void populateBaseFields(BaseEvent event, EventType eventType) {
        event.setEventType(eventType);
        event.setUserId(USER_IDS[random.nextInt(USER_IDS.length)]);
        event.setTimestamp(Instant.now().minusSeconds(random.nextInt(86400)));

        DeviceDetails deviceDetails = new DeviceDetails();
        deviceDetails.setDeviceId(UUID.randomUUID().toString());
        deviceDetails.setDeviceModel(DEVICE_MODELS[random.nextInt(DEVICE_MODELS.length)]);
        deviceDetails.setOsVersion(random.nextInt(10) + "." + random.nextInt(10));
        deviceDetails.setPlatform(PLATFORMS[random.nextInt(PLATFORMS.length)]);
        deviceDetails.setAppVersion("1." + random.nextInt(10) + "." + random.nextInt(10));

        event.setDeviceDetails(deviceDetails);
    }
}
