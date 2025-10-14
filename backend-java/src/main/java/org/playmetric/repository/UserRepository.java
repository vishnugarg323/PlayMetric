package org.playmetric.repository;

import org.playmetric.model.User;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

/**
 * Repository for User entity operations.
 * Provides CRUD operations and custom queries for user analytics.
 */
@Repository
public interface UserRepository extends MongoRepository<User, String> {
    
    /**
     * Find user by userId.
     * @param userId The unique user identifier
     * @return Optional containing the user if found
     */
    Optional<User> findByUserId(String userId);
    
    /**
     * Find all users by platform.
     * Useful for platform-specific analytics.
     */
    List<User> findByPlatform(String platform);
    
    /**
     * Find all users by app version.
     * Useful for version-specific analytics and A/B testing.
     */
    List<User> findByAppVersion(String appVersion);
    
    /**
     * Find users last seen after a specific timestamp.
     * Useful for active user analysis.
     */
    List<User> findByLastSeenAfter(Instant timestamp);
    
    /**
     * Find users first seen after a specific timestamp.
     * Useful for new user cohort analysis.
     */
    List<User> findByFirstSeenAfter(Instant timestamp);
    
    /**
     * Check if a user exists by userId.
     */
    boolean existsByUserId(String userId);
}
