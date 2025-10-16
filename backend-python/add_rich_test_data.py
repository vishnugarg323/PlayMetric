"""
Add rich test data to populate all dashboard graphs
This script generates diverse data for better visualization
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import random

# MongoDB connection - use environment variable or default
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://playmetric:N1jkHNItLKyRNLHXNTnBgEeiwYCiUBJG@gondola.proxy.rlwy.net:21458")
DB_NAME = "playmetric"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def generate_rich_test_data():
    """Generate comprehensive test data"""
    print("🎲 Generating rich test data...")
    
    # User IDs to use
    user_ids = [f"user_{i}" for i in range(1, 21)]  # 20 users
    
    # Platforms
    platforms = ["Android", "iOS", "Web"]
    
    # Event types
    event_types = ["session_start", "session_end", "level_complete", "level_fail", "purchase", "ad_watched"]
    
    now = datetime.now(timezone.utc)
    
    # Generate events over last 30 days
    events_added = 0
    
    for user_id in user_ids:
        # Each user has activity over different time ranges
        user_start_date = now - timedelta(days=random.randint(5, 30))
        num_sessions = random.randint(10, 100)
        
        for session in range(num_sessions):
            session_date = user_start_date + timedelta(
                days=random.randint(0, (now - user_start_date).days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            platform = random.choice(platforms)
            session_duration = random.randint(60, 3600)  # 1 min to 1 hour
            
            # Session start
            game_event = {
                "eventType": "GAME_SESSION_START",
                "globalParams": {
                    "userId": user_id,
                    "sessionId": f"session_{user_id}_{session}",
                    "platform": platform,
                    "timestamp": session_date,
                    "sessionDuration": session_duration
                }
            }
            db.game_events.insert_one(game_event)
            events_added += 1
            
            # Random level events within session
            levels_played = random.randint(1, 10)
            for level in range(1, levels_played + 1):
                completed = random.random() > 0.3  # 70% completion rate
                
                level_event = {
                    "eventType": "LEVEL_COMPLETE" if completed else "LEVEL_FAIL",
                    "levelNumber": random.randint(1, 50),
                    "difficulty": random.choice(["Easy", "Medium", "Hard"]),
                    "completed": completed,
                    "attempts": random.randint(1, 5),
                    "duration": random.randint(30, 600),
                    "score": random.randint(100, 5000) if completed else random.randint(0, 1000),
                    "globalParams": {
                        "userId": user_id,
                        "sessionId": f"session_{user_id}_{session}",
                        "platform": platform,
                        "timestamp": session_date + timedelta(seconds=random.randint(10, session_duration))
                    }
                }
                db.level_events.insert_one(level_event)
                events_added += 1
            
            # Random economy events (purchases, in-game currency)
            if random.random() > 0.7:  # 30% chance of purchase in session
                economy_event = {
                    "eventType": "ECONOMY_PURCHASE",
                    "itemId": f"item_{random.randint(1, 20)}",
                    "itemName": random.choice(["Gems", "Coins", "PowerUp", "Skin", "Booster"]),
                    "quantity": random.randint(1, 100),
                    "currency": random.choice(["USD", "EUR", "GBP"]),
                    "realMoneyValue": round(random.uniform(0.99, 49.99), 2) if random.random() > 0.5 else 0,
                    "virtualCurrency": random.randint(100, 5000),
                    "globalParams": {
                        "userId": user_id,
                        "sessionId": f"session_{user_id}_{session}",
                        "platform": platform,
                        "timestamp": session_date + timedelta(seconds=random.randint(10, session_duration))
                    }
                }
                db.economy_events.insert_one(economy_event)
                events_added += 1
            
            # Mission events
            if random.random() > 0.5:  # 50% chance
                mission_event = {
                    "eventType": "MISSION_COMPLETE" if random.random() > 0.3 else "MISSION_START",
                    "missionId": f"mission_{random.randint(1, 30)}",
                    "missionType": random.choice(["Daily", "Weekly", "Special"]),
                    "progress": random.randint(0, 100),
                    "rewards": [
                        {"type": "coins", "amount": random.randint(50, 500)},
                        {"type": "gems", "amount": random.randint(5, 50)}
                    ] if random.random() > 0.5 else [],
                    "globalParams": {
                        "userId": user_id,
                        "sessionId": f"session_{user_id}_{session}",
                        "platform": platform,
                        "timestamp": session_date + timedelta(seconds=random.randint(10, session_duration))
                    }
                }
                db.mission_events.insert_one(mission_event)
                events_added += 1
            
            # Ads events
            if random.random() > 0.6:  # 40% chance
                ads_event = {
                    "eventType": "ADS_WATCHED",
                    "adType": random.choice(["Rewarded", "Interstitial", "Banner"]),
                    "adNetwork": random.choice(["AdMob", "Unity", "Facebook"]),
                    "completed": random.random() > 0.2,
                    "reward": {"type": "coins", "amount": random.randint(50, 200)} if random.random() > 0.3 else None,
                    "globalParams": {
                        "userId": user_id,
                        "sessionId": f"session_{user_id}_{session}",
                        "platform": platform,
                        "timestamp": session_date + timedelta(seconds=random.randint(10, session_duration))
                    }
                }
                db.ads_events.insert_one(ads_event)
                events_added += 1
            
            # UI interaction events
            ui_actions = ["button_click", "menu_open", "settings_change", "tutorial_skip"]
            for _ in range(random.randint(0, 5)):
                ui_event = {
                    "eventType": "UI_INTERACTION",
                    "action": random.choice(ui_actions),
                    "element": random.choice(["MainMenu", "Shop", "Inventory", "Settings", "Leaderboard"]),
                    "value": random.choice([None, random.randint(1, 100)]),
                    "globalParams": {
                        "userId": user_id,
                        "sessionId": f"session_{user_id}_{session}",
                        "platform": platform,
                        "timestamp": session_date + timedelta(seconds=random.randint(10, session_duration))
                    }
                }
                db.ui_interaction_events.insert_one(ui_event)
                events_added += 1
            
            # Session end
            game_event_end = {
                "eventType": "GAME_SESSION_END",
                "globalParams": {
                    "userId": user_id,
                    "sessionId": f"session_{user_id}_{session}",
                    "platform": platform,
                    "timestamp": session_date + timedelta(seconds=session_duration),
                    "sessionDuration": session_duration
                }
            }
            db.game_events.insert_one(game_event_end)
            events_added += 1
    
    # Update user documents
    for user_id in user_ids:
        # Get user's events
        user_events = list(db.game_events.find({"globalParams.userId": user_id}))
        
        if user_events:
            timestamps = [e['globalParams']['timestamp'] for e in user_events]
            first_seen = min(timestamps)
            last_seen = max(timestamps)
            
            total_sessions = len([e for e in user_events if e['eventType'] == 'GAME_SESSION_START'])
            total_events = (
                len(list(db.game_events.find({"globalParams.userId": user_id}))) +
                len(list(db.level_events.find({"globalParams.userId": user_id}))) +
                len(list(db.economy_events.find({"globalParams.userId": user_id})))
            )
            
            # Calculate total revenue
            purchases = list(db.economy_events.find({
                "globalParams.userId": user_id,
                "realMoneyValue": {"$gt": 0}
            }))
            total_revenue = sum(p.get('realMoneyValue', 0) for p in purchases)
            
            db.users.update_one(
                {"userId": user_id},
                {
                    "$set": {
                        "userId": user_id,
                        "firstSeen": first_seen,
                        "lastSeen": last_seen,
                        "totalSessions": total_sessions,
                        "totalEvents": total_events,
                        "platform": random.choice(platforms),
                        "totalRevenue": total_revenue,
                        "deviceDetails": {
                            "os": random.choice(["Android 13", "iOS 17", "Windows 11"]),
                            "model": random.choice(["Pixel 7", "iPhone 14", "Samsung S23", "iPad Pro"]),
                            "country": random.choice(["US", "UK", "CA", "DE", "FR", "JP"])
                        }
                    }
                },
                upsert=True
            )
    
    print(f"✅ Added {events_added} events across {len(user_ids)} users")
    print(f"📊 Total events in DB: {db.game_events.count_documents({}) + db.level_events.count_documents({}) + db.economy_events.count_documents({})}")
    print(f"👥 Total users in DB: {db.users.count_documents({})}")

if __name__ == "__main__":
    generate_rich_test_data()
    client.close()
    print("\n✨ Done! Refresh the dashboard to see the new data.")
