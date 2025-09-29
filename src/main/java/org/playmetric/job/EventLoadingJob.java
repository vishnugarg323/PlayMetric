package org.playmetric.job;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.playmetric.model.BaseEvent;
import org.playmetric.service.EventService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Stream;

@Slf4j
@Component
@Order(2)
@Profile("data-load")
@RequiredArgsConstructor
public class EventLoadingJob implements CommandLineRunner {
    private final EventService eventService;
    private final ObjectMapper objectMapper;
    private static final String DATA_DIR = "test-data";

    @Override
    public void run(String... args) throws Exception {
        Path dataDir = Paths.get(DATA_DIR);
        if (!Files.exists(dataDir)) {
            log.warn("Test data directory not found. Please run the generator job first.");
            return;
        }

        try (Stream<Path> paths = Files.list(dataDir)) {
            paths.filter(path -> path.toString().endsWith(".json"))
                 .forEach(this::processEventFile);
        }
    }

    private void processEventFile(Path filePath) {
        try {
            log.info("Processing event file: {}", filePath);
            List<BaseEvent> events = objectMapper.readValue(
                filePath.toFile(),
                new TypeReference<List<BaseEvent>>() {}
            );

            events.forEach(event -> {
                try {
                    eventService.saveEvent(event);
                    log.debug("Processed event: {}", event.getId());
                } catch (Exception e) {
                    log.error("Error processing event: {}", e.getMessage());
                }
            });

            log.info("Successfully processed {} events from {}", events.size(), filePath);
        } catch (Exception e) {
            log.error("Error processing file {}: {}", filePath, e.getMessage());
        }
    }
}
