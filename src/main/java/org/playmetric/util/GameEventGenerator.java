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
        List<Object> events = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            events.add(createEvent(eventType));
        }
        objectMapper.writerWithDefaultPrettyPrinter().writeValue(new File(filePath), events);
    }


    private Object createEvent(EventType eventType) {
        String id = UUID.randomUUID().toString();
        String userId = USER_IDS[random.nextInt(USER_IDS.length)];
        DeviceDetails deviceDetails = new DeviceDetails(
            UUID.randomUUID().toString(),
            DEVICE_MODELS[random.nextInt(DEVICE_MODELS.length)],
            random.nextInt(10) + "." + random.nextInt(10),
            PLATFORMS[random.nextInt(PLATFORMS.length)],
            "1." + random.nextInt(10) + "." + random.nextInt(10)
        );
        Instant timestamp = Instant.now().minusSeconds(random.nextInt(86400));

        return switch (eventType) {
            case GAME_START, GAME_END -> new GameEvent(
                id,
                userId,
                deviceDetails,
                timestamp,
                eventType,
                UUID.randomUUID().toString(),
                "pattern_" + random.nextInt(5),
                random.nextInt(3600)
            );
            case LEVEL_START, LEVEL_END, LEVEL_FAILED -> new LevelEvent(
                id,
                userId,
                deviceDetails,
                timestamp,
                eventType,
                LEVEL_IDS[random.nextInt(LEVEL_IDS.length)],
                random.nextInt(5) + 1,
                eventType == EventType.LEVEL_FAILED ? "reason_" + random.nextInt(3) : null,
                random.nextInt(600),
                eventType == EventType.LEVEL_END
            );
            case ECONOMY_TRANSACTION -> new EconomyEvent(
                id,
                userId,
                deviceDetails,
                timestamp,
                eventType,
                UUID.randomUUID().toString(),
                CURRENCIES[random.nextInt(CURRENCIES.length)],
                random.nextDouble() * 1000,
                random.nextBoolean() ? "PURCHASE" : "SELL",
                random.nextDouble() * 100
            );
            case MISSION_START, MISSION_END -> new MissionEvent(
                id,
                userId,
                deviceDetails,
                timestamp,
                eventType,
                random.nextBoolean() ? "DAILY" : "MONTHLY",
                UUID.randomUUID().toString(),
                eventType == EventType.MISSION_END,
                random.nextInt(3600)
            );
            case AD_LOADED, AD_SHOWN, AD_COMPLETED, AD_CLOSED, AD_REVENUE -> new AdsEvent(
                id,
                userId,
                deviceDetails,
                timestamp,
                eventType,
                eventType.name(),
                random.nextDouble() * 10,
                UUID.randomUUID().toString()
            );
            case UI_INTERACTION -> new UIInteractionEvent(
                id,
                userId,
                deviceDetails,
                timestamp,
                eventType,
                "CLICK",
                "Button pressed"
            );
        };
    }
}
