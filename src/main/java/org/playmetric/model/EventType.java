package org.playmetric.model;

/**
 * Comprehensive enumeration of game event types optimized for AI-driven analytics.
 * 
 * <p>Event categories:
 * <ul>
 *   <li><b>SESSION:</b> Game session lifecycle events</li>
 *   <li><b>LEVEL:</b> Level progression and performance events</li>
 *   <li><b>GAME:</b> Game-specific events and mechanics</li>
 *   <li><b>ECONOMY:</b> In-game economy and monetization events</li>
 *   <li><b>SOCIAL:</b> Social interaction and multiplayer events</li>
 *   <li><b>ACHIEVEMENT:</b> Achievement and progression milestone events</li>
 *   <li><b>AD:</b> Advertisement interaction events</li>
 *   <li><b>UI:</b> User interface interaction events</li>
 *   <li><b>PERFORMANCE:</b> Technical performance and error events</li>
 *   <li><b>TUTORIAL:</b> Tutorial and onboarding events</li>
 * </ul>
 * 
 * <p>These events enable AI analysis for:
 * - Level difficulty calibration
 * - Churn prediction and prevention
 * - User engagement scoring
 * - Monetization optimization
 * - Content recommendation
 * - Bug detection and performance monitoring
 */
public enum EventType {
    
    // ========== SESSION EVENTS ==========
    /** User starts a new game session */
    SESSION_START,
    /** User ends a game session normally */
    SESSION_END,
    /** User's session ends due to timeout or inactivity */
    SESSION_TIMEOUT,
    /** User pauses the game */
    SESSION_PAUSE,
    /** User resumes the game from pause */
    SESSION_RESUME,
    /** User's session is interrupted (background, call, etc.) */
    SESSION_INTERRUPT,
    
    // ========== LEVEL EVENTS ==========
    /** User starts a level */
    LEVEL_START,
    /** User completes a level successfully */
    LEVEL_COMPLETE,
    /** User fails a level */
    LEVEL_FAIL,
    /** User quits/abandons a level mid-play */
    LEVEL_QUIT,
    /** User restarts a level */
    LEVEL_RESTART,
    /** User unlocks a new level */
    LEVEL_UNLOCK,
    /** User reaches a checkpoint within a level */
    LEVEL_CHECKPOINT,
    /** User skips a level (if feature exists) */
    LEVEL_SKIP,
    
    // ========== GAME EVENTS ==========
    /** Generic game start event */
    GAME_START,
    /** Generic game end event */
    GAME_END,
    /** User completes the entire game */
    GAME_COMPLETE,
    /** User defeats a boss or major enemy */
    GAME_BOSS_DEFEAT,
    /** User is defeated by boss or major enemy */
    GAME_BOSS_FAIL,
    /** User collects an item */
    GAME_ITEM_COLLECT,
    /** User uses an item */
    GAME_ITEM_USE,
    /** User loses health/damage taken */
    GAME_DAMAGE_TAKEN,
    /** Player character dies/loses life */
    GAME_PLAYER_DEATH,
    /** Player respawns */
    GAME_PLAYER_RESPAWN,
    /** Player scores points */
    GAME_SCORE_UPDATE,
    /** Player achieves high score */
    GAME_HIGH_SCORE,
    /** Player uses a power-up */
    GAME_POWERUP_USE,
    /** Power-up expires */
    GAME_POWERUP_EXPIRE,
    
    // ========== MISSION/QUEST EVENTS ==========
    /** User starts a mission/quest */
    MISSION_START,
    /** User completes a mission/quest */
    MISSION_COMPLETE,
    /** User fails a mission/quest */
    MISSION_FAIL,
    /** User abandons a mission/quest */
    MISSION_ABANDON,
    /** User claims mission rewards */
    MISSION_REWARD_CLAIM,
    
    // ========== ECONOMY EVENTS ==========
    /** Generic economy transaction */
    ECONOMY_TRANSACTION,
    /** User purchases virtual currency */
    ECONOMY_CURRENCY_PURCHASE,
    /** User spends virtual currency */
    ECONOMY_CURRENCY_SPEND,
    /** User earns virtual currency through gameplay */
    ECONOMY_CURRENCY_EARN,
    /** User purchases an in-app item */
    ECONOMY_IAP_PURCHASE,
    /** IAP purchase fails */
    ECONOMY_IAP_FAIL,
    /** User views the shop/store */
    ECONOMY_SHOP_VIEW,
    /** User upgrades an item/character */
    ECONOMY_UPGRADE,
    /** User unlocks a character/skin/feature */
    ECONOMY_UNLOCK,
    /** User receives a reward (daily bonus, gift, etc.) */
    ECONOMY_REWARD_RECEIVED,
    
    // ========== SOCIAL EVENTS ==========
    /** User invites a friend */
    SOCIAL_INVITE_SENT,
    /** User accepts friend invite */
    SOCIAL_INVITE_ACCEPTED,
    /** User shares content to social media */
    SOCIAL_SHARE,
    /** User joins a guild/clan/team */
    SOCIAL_GUILD_JOIN,
    /** User leaves a guild/clan/team */
    SOCIAL_GUILD_LEAVE,
    /** User sends a chat message */
    SOCIAL_CHAT_SEND,
    /** User participates in multiplayer match */
    SOCIAL_MULTIPLAYER_JOIN,
    /** User wins multiplayer match */
    SOCIAL_MULTIPLAYER_WIN,
    /** User loses multiplayer match */
    SOCIAL_MULTIPLAYER_LOSE,
    
    // ========== ACHIEVEMENT EVENTS ==========
    /** User unlocks an achievement */
    ACHIEVEMENT_UNLOCK,
    /** User progresses toward an achievement */
    ACHIEVEMENT_PROGRESS,
    /** User reaches a new player level/rank */
    ACHIEVEMENT_LEVEL_UP,
    /** User completes a collection */
    ACHIEVEMENT_COLLECTION_COMPLETE,
    /** User earns a badge/trophy */
    ACHIEVEMENT_BADGE_EARN,
    
    // ========== AD EVENTS ==========
    /** Ad is loaded */
    AD_LOADED,
    /** Ad is shown to user */
    AD_SHOWN,
    /** User watches ad to completion */
    AD_COMPLETED,
    /** User closes/skips ad */
    AD_CLOSED,
    /** Ad generates revenue */
    AD_REVENUE,
    /** Ad fails to load */
    AD_LOAD_FAIL,
    /** User clicks on ad */
    AD_CLICK,
    /** Rewarded ad is shown */
    AD_REWARDED_SHOWN,
    /** User receives reward from ad */
    AD_REWARDED_COMPLETE,
    
    // ========== UI EVENTS ==========
    /** Generic UI interaction */
    UI_INTERACTION,
    /** User clicks a button */
    UI_BUTTON_CLICK,
    /** User opens a menu */
    UI_MENU_OPEN,
    /** User closes a menu */
    UI_MENU_CLOSE,
    /** User opens settings */
    UI_SETTINGS_OPEN,
    /** User changes a setting */
    UI_SETTINGS_CHANGE,
    /** User views tutorial/help */
    UI_TUTORIAL_VIEW,
    /** User dismisses a dialog */
    UI_DIALOG_DISMISS,
    
    // ========== TUTORIAL EVENTS ==========
    /** User starts tutorial */
    TUTORIAL_START,
    /** User completes tutorial */
    TUTORIAL_COMPLETE,
    /** User skips tutorial */
    TUTORIAL_SKIP,
    /** User views a tutorial step */
    TUTORIAL_STEP_VIEW,
    /** User completes a tutorial step */
    TUTORIAL_STEP_COMPLETE,
    
    // ========== PERFORMANCE EVENTS ==========
    /** Application error occurred */
    PERFORMANCE_ERROR,
    /** Application crashes */
    PERFORMANCE_CRASH,
    /** Low FPS detected */
    PERFORMANCE_LOW_FPS,
    /** High memory usage detected */
    PERFORMANCE_HIGH_MEMORY,
    /** Network error */
    PERFORMANCE_NETWORK_ERROR,
    /** Loading time measurement */
    PERFORMANCE_LOAD_TIME,
    
    // ========== ENGAGEMENT EVENTS ==========
    /** User logs in */
    ENGAGEMENT_LOGIN,
    /** User logs out */
    ENGAGEMENT_LOGOUT,
    /** User returns after being away (retention) */
    ENGAGEMENT_RETURN,
    /** Daily login bonus claimed */
    ENGAGEMENT_DAILY_BONUS,
    /** User completes daily challenge */
    ENGAGEMENT_DAILY_CHALLENGE,
    /** User views a specific screen/feature */
    ENGAGEMENT_SCREEN_VIEW,
    
    // ========== CUSTOM EVENTS ==========
    /** Custom event type 1 - can be used for game-specific events */
    CUSTOM_EVENT_1,
    /** Custom event type 2 - can be used for game-specific events */
    CUSTOM_EVENT_2,
    /** Custom event type 3 - can be used for game-specific events */
    CUSTOM_EVENT_3
}
