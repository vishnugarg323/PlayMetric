package org.playmetric.testutil.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
@ConfigurationProperties(prefix = "event.generator.target")
@Data
public class EventGeneratorConfig {
    private String url;
    private int batchSize;
    private int totalEvents;
    private long delayBetweenBatchesMs;

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
