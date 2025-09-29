package org.playmetric.service.config;

import com.mongodb.client.MongoClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@Configuration
@EnableMongoRepositories(
    basePackages = "org.playmetric.service.repository.events",
    mongoTemplateRef = "eventMongoTemplate"
)
public class EventMongoConfig {

    @Primary
    @Bean(name = "eventMongoTemplate")
    public MongoTemplate eventMongoTemplate(MongoClient mongoClient) {
        return new MongoTemplate(mongoClient, "playmetric");
    }
}
