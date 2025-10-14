package org.playmetric.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig {
    public CorsConfig() {
        org.slf4j.LoggerFactory.getLogger(CorsConfig.class).info("CORS config initialized: allowing all origins, headers, methods");
    }
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**")
                        .allowedOriginPatterns("*")
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                        .allowedHeaders("*")
                        .exposedHeaders("Authorization", "Link", "X-Total-Count", "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials")
                        .allowCredentials(false)
                        .maxAge(3600);
            }
        };
    }
}