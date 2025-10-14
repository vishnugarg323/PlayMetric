package org.playmetric.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI playMetricOpenAPI() {
    return new OpenAPI()
        .info(new Info()
            .title("PlayMetric Game Analytics API")
            .description("API for tracking and analyzing game events")
            .version("1.0"))
        .addServersItem(new io.swagger.v3.oas.models.servers.Server()
            .url("https://playmetric-production.up.railway.app")
            .description("Production Railway HTTPS server"));
    }
}
