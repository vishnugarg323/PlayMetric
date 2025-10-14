package org.playmetric.service;

import org.playmetric.model.GlobalEventParameters;
import org.playmetric.model.User;
import org.playmetric.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

/**
 * Service for managing user lifecycle and tracking user activity.
 * Automatically creates users when first event is received and updates
 * user information on subsequent events.
 * 
 * <p>This service is central to user analytics and provides:
 * <ul>
 *   <li>Automatic user creation from event data</li>
 *   <li>User activity tracking and session management</li>
 *   <li>User retention and churn analysis support</li>
 *   <li>Cross-device user tracking</li>
 * </ul>
 */
@Service
public class UserService {
    
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
    
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Ensures user exists in the database. Creates user if not found, updates if exists.
     * This method is called for every event to maintain user state.
     * 
     * @param globalParams Global event parameters containing user information
     * @return The user entity (created or updated)
     */
    @Transactional
    public User ensureUserExists(GlobalEventParameters globalParams) {
        String userId = globalParams.userId();
        
        Optional<User> existingUser = userRepository.findByUserId(userId);
        
        if (existingUser.isPresent()) {
            // User exists - update their information
            User user = existingUser.get();
            user.updateFromGlobalParams(globalParams);
            User savedUser = userRepository.save(user);
            logger.debug("Updated user: {} - Total events: {}, Total sessions: {}", 
                userId, savedUser.getTotalEvents(), savedUser.getTotalSessions());
            return savedUser;
        } else {
            // User doesn't exist - create new user
            User newUser = User.fromGlobalParams(globalParams);
            User savedUser = userRepository.save(newUser);
            logger.info("Created new user: {} from device: {} on platform: {}", 
                userId, globalParams.deviceId(), globalParams.platform());
            return savedUser;
        }
    }

    /**
     * Gets a user by their userId.
     * 
     * @param userId The unique user identifier
     * @return Optional containing the user if found
     */
    public Optional<User> getUserById(String userId) {
        return userRepository.findByUserId(userId);
    }

    /**
     * Gets all users.
     * 
     * @return List of all users
     */
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    /**
     * Gets all users on a specific platform.
     * 
     * @param platform Platform identifier (e.g., "iOS", "Android")
     * @return List of users on the specified platform
     */
    public List<User> getUsersByPlatform(String platform) {
        return userRepository.findByPlatform(platform);
    }

    /**
     * Gets all users using a specific app version.
     * 
     * @param appVersion App version string
     * @return List of users on the specified app version
     */
    public List<User> getUsersByAppVersion(String appVersion) {
        return userRepository.findByAppVersion(appVersion);
    }

    /**
     * Gets active users (users who were active after a specific timestamp).
     * Useful for retention analysis.
     * 
     * @param since Timestamp to check activity after
     * @return List of active users
     */
    public List<User> getActiveUsersSince(Instant since) {
        return userRepository.findByLastSeenAfter(since);
    }

    /**
     * Gets new users (users who first appeared after a specific timestamp).
     * Useful for cohort analysis.
     * 
     * @param since Timestamp to check first appearance after
     * @return List of new users
     */
    public List<User> getNewUsersSince(Instant since) {
        return userRepository.findByFirstSeenAfter(since);
    }

    /**
     * Checks if a user exists.
     * 
     * @param userId The unique user identifier
     * @return true if user exists, false otherwise
     */
    public boolean userExists(String userId) {
        return userRepository.existsByUserId(userId);
    }

    /**
     * Gets total user count.
     * 
     * @return Total number of users
     */
    public long getTotalUserCount() {
        return userRepository.count();
    }
}
