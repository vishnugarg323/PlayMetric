package org.playmetric.job;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.playmetric.model.EventType;
import org.playmetric.util.GameEventGenerator;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@Slf4j
@Component
@RequiredArgsConstructor
public class TestDataGeneratorJob implements CommandLineRunner {
    private final GameEventGenerator eventGenerator;
    private static final String DATA_DIR = "test-data";
    private static final int EVENTS_PER_TYPE = 500;

    @Override
    public void run(String... args) throws Exception {
        Path dataDir = Paths.get(DATA_DIR);
        if (!Files.exists(dataDir)) {
            Files.createDirectory(dataDir);
        }

        for (EventType eventType : EventType.values()) {
            String fileName = String.format("%s/%s_events.json", DATA_DIR, eventType.name().toLowerCase());
            log.info("Generating {} events for type {}", EVENTS_PER_TYPE, eventType);
            eventGenerator.generateAndSaveEvents(fileName, EVENTS_PER_TYPE, eventType);
        }
    }
}
