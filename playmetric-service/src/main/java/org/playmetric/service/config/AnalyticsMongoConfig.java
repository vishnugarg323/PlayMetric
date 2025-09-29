package org.playmetric.service.config;

import com.mongodb.client.MongoClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@Configuration
@EnableMongoRepositories(
    basePackages = "org.playmetric.service.repository.analytics",
    mongoTemplateRef = "analyticsMongoTemplate"
)
public class AnalyticsMongoConfig {

    @Bean(name = "analyticsMongoTemplate")
    public MongoTemplate analyticsMongoTemplate(MongoClient mongoClient) {
        return new MongoTemplate(mongoClient, "playmetric_analytics");
    }
}
