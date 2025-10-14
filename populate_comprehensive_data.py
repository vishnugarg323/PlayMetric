"""
Comprehensive Data Population Script for PAIME
Generates realistic game analytics data with proper user profiles
"""
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
import uuid
from collections import defaultdict

# MongoDB Configuration - Railway Hosted
MONGODB_URI = "mongodb://mongo:gSFyjoeBNGrWpElewAfFLzloUYmSyqRm@gondola.proxy.rlwy.net:21458/playmetric?authSource=admin"
DATABASE_NAME = "playmetric"

# Game Configuration
GAME_NAME = "Test Game"
NUM_USERS = 10
EVENTS_PER_USER = 10000
NUM_LEVELS = 15  # Increased levels
PLATFORMS = ['ANDROID', 'IOS', 'WEB']
CURRENCIES = ['COINS', 'GEMS', 'STARS', 'GOLD']
AD_TYPES = ['REWARDED', 'INTERSTITIAL', 'BANNER']

# User archetypes for realistic behavior
USER_ARCHETYPES = {
    'whale': {'sessions_range': (100, 200), 'purchase_probability': 0.15, 'churn_risk': 0.1},
    'engaged': {'sessions_range': (80, 150), 'purchase_probability': 0.05, 'churn_risk': 0.2},
    'casual': {'sessions_range': (30, 80), 'purchase_probability': 0.02, 'churn_risk': 0.4},
    'at_risk': {'sessions_range': (10, 30), 'purchase_probability': 0.01, 'churn_risk': 0.7},
    'dormant': {'sessions_range': (5, 15), 'purchase_probability': 0.005, 'churn_risk': 0.9}
}

def generate_user_profile(user_index, start_date):
    """Generate a realistic user profile"""
    archetype = random.choices(
        ['whale', 'engaged', 'casual', 'at_risk', 'dormant'],
        weights=[0.05, 0.25, 0.40, 0.20, 0.10]
    )[0]
    
    user_id = f"test_user_{user_index+1:03d}"
    platform = random.choice(PLATFORMS)
    registration_date = start_date + timedelta(days=random.randint(0, 25))
    
    # Calculate activity based on archetype
    arch_config = USER_ARCHETYPES[archetype]
    total_sessions = random.randint(*arch_config['sessions_range'])
    
    # Recent activity determines lastSeen
    if archetype == 'dormant':
        last_seen = datetime.now() - timedelta(days=random.randint(15, 30))
    elif archetype == 'at_risk':
        last_seen = datetime.now() - timedelta(days=random.randint(5, 10))
    else:
        last_seen = datetime.now() - timedelta(hours=random.randint(1, 48))
    
    return {
        'userId': user_id,
        'platform': platform,
        'registrationDate': registration_date,
        'lastSeen': last_seen,
        'archetype': archetype,
        'totalSessions': total_sessions,
        'deviceId': f"device_{user_id}_{random.randint(1000, 9999)}",
        'deviceModel': random.choice(['Samsung Galaxy S21', 'iPhone 13', 'Pixel 6', 'OnePlus 9', 'iPad Air']),
        'osVersion': random.choice(['Android 12', 'iOS 15', 'Android 11', 'iOS 16', 'Web']),
        'country': random.choice(['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP', 'BR', 'IN', 'CN']),
        'totalEvents': 0,  # Will be calculated
        'totalPurchases': 0,  # Will be calculated
        'totalSpent': 0.0,  # Will be calculated
        'maxLevelReached': 0,  # Will be calculated
        'completedLevels': 0,  # Will be calculated
    }

def generate_device_details():
    """Generate random device details"""
    return {
        'deviceModel': random.choice(['Samsung Galaxy S21', 'iPhone 13', 'Pixel 6', 'OnePlus 9', 'iPad Air']),
        'osVersion': random.choice(['Android 12', 'iOS 15', 'Android 11', 'iOS 16']),
        'appVersion': f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 20)}"
    }

def generate_global_params(user, session_id, timestamp):
    """Generate global parameters for events"""
    return {
        'userId': user['userId'],
        'deviceId': user['deviceId'],
        'platform': user['platform'],
        'sessionId': session_id,
        'timestamp': timestamp.isoformat() + 'Z',
        'gameName': GAME_NAME,
        'deviceDetails': {
            'deviceModel': user['deviceModel'],
            'osVersion': user['osVersion'],
            'appVersion': random.choice(['1.0.0', '1.1.0', '1.2.0'])
        }
    }

def generate_level_event(event_type, level_id, global_params, user_archetype):
    """Generate level event with realistic behavior"""
    event = {
        'globalParams': global_params,
        'eventType': event_type,
        'levelId': level_id,
        'timestamp': global_params['timestamp']
    }
    
    # Make lower levels easier, higher levels harder
    difficulty_multiplier = 1 + (level_id * 0.15)
    
    if event_type == 'LEVEL_COMPLETE':
        # Whale and engaged users perform better
        if user_archetype in ['whale', 'engaged']:
            score_range = (int(3000 * difficulty_multiplier), int(5000 * difficulty_multiplier))
            stars = random.choices([1, 2, 3], weights=[0.1, 0.2, 0.7])[0]
            perfect = random.choice([True, False]) if stars == 3 else False
        else:
            score_range = (int(1000 * difficulty_multiplier), int(3500 * difficulty_multiplier))
            stars = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]
            perfect = False
        
        event.update({
            'score': random.randint(*score_range),
            'stars': stars,
            'completed': True,
            'timeTaken': int(random.randint(45, 180) * difficulty_multiplier),
            'perfectPlay': perfect
        })
    elif event_type == 'LEVEL_START':
        event.update({
            'attemptNumber': random.randint(1, int(3 * difficulty_multiplier))
        })
    elif event_type == 'LEVEL_FAILED':
        event.update({
            'score': random.randint(int(100 * difficulty_multiplier), int(2000 * difficulty_multiplier)),
            'timeTaken': int(random.randint(30, 150) * difficulty_multiplier),
            'failureReason': random.choice(['TIME_OUT', 'HEALTH_DEPLETED', 'OBJECTIVE_FAILED'])
        })
    
    return event

def generate_economy_event(event_type, global_params, user_archetype):
    """Generate economy event based on user behavior"""
    currency = random.choice(CURRENCIES)
    
    # Whales spend more
    if user_archetype == 'whale':
        amount = random.randint(100, 2000)
    elif user_archetype == 'engaged':
        amount = random.randint(50, 1000)
    else:
        amount = random.randint(10, 500)
    
    event = {
        'globalParams': global_params,
        'eventType': event_type,
        'currencyType': currency,
        'amount': amount,
        'balanceAfter': random.randint(0, 10000),
        'timestamp': global_params['timestamp']
    }
    
    if event_type == 'ECONOMY_PURCHASE':
        # Real money purchases
        purchase_config = USER_ARCHETYPES[user_archetype]
        if random.random() < purchase_config['purchase_probability']:
            event['priceInRealMoney'] = random.choice([0.99, 1.99, 4.99, 9.99, 19.99, 49.99])
        else:
            event['priceInRealMoney'] = None  # In-game currency purchase
        
        event.update({
            'itemId': f"item_{random.randint(1, 100)}",
            'itemName': random.choice(['Power-up Pack', 'Extra Life', 'Booster', 'Shield', 'Time Extension', 'Coin Pack', 'Gem Bundle']),
            'transactionId': str(uuid.uuid4())
        })
    elif event_type == 'ECONOMY_EARN':
        event['source'] = random.choice(['LEVEL_COMPLETE', 'DAILY_REWARD', 'ACHIEVEMENT', 'AD_REWARD', 'MISSION_COMPLETE'])
    elif event_type == 'ECONOMY_SPEND':
        event['spentOn'] = random.choice(['POWER_UP', 'UNLOCK_LEVEL', 'BOOST', 'CONTINUE', 'COSMETIC'])
    
    return event

def generate_game_event(event_type, global_params):
    """Generate game start/end event"""
    event = {
        'globalParams': global_params,
        'eventType': event_type,
        'timestamp': global_params['timestamp']
    }
    
    if event_type == 'GAME_END':
        event['sessionDuration'] = random.randint(120, 3600)
    
    return event

def generate_mission_event(event_type, global_params):
    """Generate mission event"""
    mission_id = random.randint(1, 30)
    event = {
        'globalParams': global_params,
        'eventType': event_type,
        'missionId': mission_id,
        'missionName': f"Complete {random.choice(['5 levels', '10 levels', 'daily challenge', 'boss fight', 'collect 100 coins'])}",
        'timestamp': global_params['timestamp']
    }
    
    if event_type == 'MISSION_COMPLETE':
        event.update({
            'reward': random.randint(100, 1000),
            'completed': True
        })
    
    return event

def generate_ads_event(global_params):
    """Generate ads event"""
    ad_type = random.choice(AD_TYPES)
    event = {
        'globalParams': global_params,
        'eventType': 'ADS_IMPRESSION',
        'adType': ad_type,
        'adProvider': random.choice(['AdMob', 'Unity Ads', 'Facebook Audience', 'IronSource']),
        'timestamp': global_params['timestamp']
    }
    
    if ad_type == 'REWARDED':
        completed = random.choice([True, True, True, False])  # 75% completion rate
        event.update({
            'completed': completed,
            'rewardAmount': 50 if completed else 0,
            'rewardType': random.choice(CURRENCIES) if completed else None
        })
    
    return event

def generate_ui_event(global_params):
    """Generate UI interaction event"""
    return {
        'globalParams': global_params,
        'eventType': 'UI_INTERACTION',
        'uiElement': random.choice(['BUTTON_PLAY', 'BUTTON_SHOP', 'BUTTON_SETTINGS', 'MENU_LEVELS', 'POPUP_OFFER', 'SLIDER_VOLUME']),
        'action': random.choice(['CLICK', 'SWIPE', 'LONG_PRESS', 'DRAG']),
        'timestamp': global_params['timestamp']
    }

def insert_events_batch(db, collection_name, events):
    """Insert events in batch"""
    if events:
        collection = db[collection_name]
        result = collection.insert_many(events)
        return len(result.inserted_ids)
    return 0

def populate_database():
    """Main function to populate database with comprehensive data"""
    print("🚀 Starting comprehensive database population...")
    print(f"📊 Configuration:")
    print(f"   - Users: {NUM_USERS}")
    print(f"   - Events per user: ~{EVENTS_PER_USER}")
    print(f"   - Levels: {NUM_LEVELS}")
    print(f"   - Game: {GAME_NAME}\n")
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
        db = client[DATABASE_NAME]
        
        # Test connection
        client.server_info()
        print("✅ Connected to Railway MongoDB successfully!\n")
        
        # Clear existing data
        print("🧹 Clearing existing collections...")
        collections = ['users', 'level_events', 'game_events', 'economy_events', 
                      'mission_events', 'ads_events', 'ui_interaction_events']
        for coll in collections:
            db[coll].delete_many({})
        print("✅ Collections cleared!\n")
        
        # Generate users
        start_date = datetime.now() - timedelta(days=30)
        users = [generate_user_profile(i, start_date) for i in range(NUM_USERS)]
        print(f"👥 Generated {len(users)} users with realistic archetypes\n")
        
        # Track events
        all_level_events = []
        all_game_events = []
        all_economy_events = []
        all_mission_events = []
        all_ads_events = []
        all_ui_events = []
        
        # Track user statistics
        user_stats = defaultdict(lambda: {
            'total_events': 0,
            'total_purchases': 0,
            'total_spent': 0.0,
            'max_level': 0,
            'completed_levels': set()
        })
        
        # Generate events for each user
        total_events = 0
        for idx, user in enumerate(users):
            print(f"⚙️  Processing user {idx+1}/{NUM_USERS}: {user['userId']} ({user['archetype']})...")
            
            user_id = user['userId']
            archetype = user['archetype']
            current_date = user['registrationDate']
            
            # Calculate number of sessions based on archetype
            num_sessions = user['totalSessions']
            events_per_session = EVENTS_PER_USER // num_sessions
            
            # User's level progression
            current_level = 1
            max_level_reached = 1
            
            for session_num in range(num_sessions):
                session_id = f"session_{user_id}_{session_num}"
                
                # Simulate time passing
                if archetype == 'dormant':
                    # Less frequent sessions
                    current_date += timedelta(days=random.randint(1, 5))
                elif archetype == 'at_risk':
                    current_date += timedelta(days=random.randint(0, 3))
                else:
                    current_date += timedelta(hours=random.randint(3, 48))
                
                # Don't go beyond now
                if current_date > datetime.now():
                    break
                
                # Session start
                global_params = generate_global_params(user, session_id, current_date)
                all_game_events.append(generate_game_event('GAME_START', global_params))
                
                # Generate events within session
                for _ in range(events_per_session):
                    event_time = current_date + timedelta(seconds=random.randint(0, 1800))
                    global_params = generate_global_params(user, session_id, event_time)
                    
                    # Weighted event distribution
                    event_choice = random.choices(
                        ['level', 'economy', 'mission', 'ads', 'ui'],
                        weights=[0.50, 0.25, 0.10, 0.08, 0.07]
                    )[0]
                    
                    if event_choice == 'level':
                        # Level progression logic
                        level_event_type = random.choices(
                            ['LEVEL_START', 'LEVEL_COMPLETE', 'LEVEL_FAILED'],
                            weights=[0.40, 0.35, 0.25]
                        )[0]
                        
                        if level_event_type == 'LEVEL_START':
                            event = generate_level_event('LEVEL_START', current_level, global_params, archetype)
                            all_level_events.append(event)
                        
                        elif level_event_type == 'LEVEL_COMPLETE':
                            event = generate_level_event('LEVEL_COMPLETE', current_level, global_params, archetype)
                            all_level_events.append(event)
                            user_stats[user_id]['completed_levels'].add(current_level)
                            
                            # Progress to next level (whales and engaged users progress faster)
                            if archetype in ['whale', 'engaged'] or random.random() > 0.3:
                                current_level = min(current_level + 1, NUM_LEVELS)
                                max_level_reached = max(max_level_reached, current_level)
                        
                        else:  # LEVEL_FAILED
                            event = generate_level_event('LEVEL_FAILED', current_level, global_params, archetype)
                            all_level_events.append(event)
                    
                    elif event_choice == 'economy':
                        eco_type = random.choice(['ECONOMY_PURCHASE', 'ECONOMY_EARN', 'ECONOMY_SPEND'])
                        event = generate_economy_event(eco_type, global_params, archetype)
                        all_economy_events.append(event)
                        
                        if eco_type == 'ECONOMY_PURCHASE' and event.get('priceInRealMoney'):
                            user_stats[user_id]['total_purchases'] += 1
                            user_stats[user_id]['total_spent'] += event['priceInRealMoney']
                    
                    elif event_choice == 'mission':
                        mission_type = random.choice(['MISSION_START', 'MISSION_COMPLETE'])
                        event = generate_mission_event(mission_type, global_params)
                        all_mission_events.append(event)
                    
                    elif event_choice == 'ads':
                        event = generate_ads_event(global_params)
                        all_ads_events.append(event)
                    
                    elif event_choice == 'ui':
                        event = generate_ui_event(global_params)
                        all_ui_events.append(event)
                    
                    user_stats[user_id]['total_events'] += 1
                    total_events += 1
                
                # Session end
                end_time = current_date + timedelta(minutes=random.randint(5, 60))
                global_params = generate_global_params(user, session_id, end_time)
                all_game_events.append(generate_game_event('GAME_END', global_params))
                
                user_stats[user_id]['max_level'] = max_level_reached
            
            print(f"   ✅ Generated {user_stats[user_id]['total_events']} events, max level: {max_level_reached}")
        
        # Update users with calculated statistics
        print(f"\n💾 Updating user profiles with statistics...")
        for user in users:
            user_id = user['userId']
            stats = user_stats[user_id]
            user['totalEvents'] = stats['total_events']
            user['totalPurchases'] = stats['total_purchases']
            user['totalSpent'] = round(stats['total_spent'], 2)
            user['maxLevelReached'] = stats['max_level']
            user['completedLevels'] = len(stats['completed_levels'])
        
        # Insert all data
        print(f"\n💾 Inserting data to Railway MongoDB...")
        
        # Insert users
        if users:
            db.users.insert_many(users)
            print(f"   ✅ Inserted {len(users)} users")
        
        # Insert events in batches
        print(f"   💾 Inserting events...")
        level_count = insert_events_batch(db, 'level_events', all_level_events)
        game_count = insert_events_batch(db, 'game_events', all_game_events)
        economy_count = insert_events_batch(db, 'economy_events', all_economy_events)
        mission_count = insert_events_batch(db, 'mission_events', all_mission_events)
        ads_count = insert_events_batch(db, 'ads_events', all_ads_events)
        ui_count = insert_events_batch(db, 'ui_interaction_events', all_ui_events)
        
        print(f"\n🎉 Database population complete!")
        print(f"📈 Total events created: {total_events:,}")
        
        print(f"\n📊 Collection Statistics:")
        print(f"   - users: {len(users):,}")
        print(f"   - level_events: {level_count:,}")
        print(f"   - game_events: {game_count:,}")
        print(f"   - economy_events: {economy_count:,}")
        print(f"   - mission_events: {mission_count:,}")
        print(f"   - ads_events: {ads_count:,}")
        print(f"   - ui_interaction_events: {ui_count:,}")
        
        # User archetype distribution
        print(f"\n👥 User Archetype Distribution:")
        archetype_counts = defaultdict(int)
        for user in users:
            archetype_counts[user['archetype']] += 1
        for arch, count in sorted(archetype_counts.items()):
            print(f"   - {arch}: {count} users")
        
        # Revenue stats
        total_revenue = sum(u['totalSpent'] for u in users)
        paying_users = len([u for u in users if u['totalSpent'] > 0])
        print(f"\n💰 Revenue Statistics:")
        print(f"   - Total Revenue: ${total_revenue:.2f}")
        print(f"   - Paying Users: {paying_users}/{len(users)}")
        print(f"   - ARPPU: ${(total_revenue/paying_users if paying_users > 0 else 0):.2f}")
        
        # Level distribution
        print(f"\n🎮 Level Progression:")
        level_pipeline = [
            {'$group': {'_id': '$levelId', 'count': {'$sum': 1}}},
            {'$sort': {'_id': 1}}
        ]
        level_dist = list(db.level_events.aggregate(level_pipeline))
        for level in level_dist[:5]:
            print(f"   - Level {level['_id']}: {level['count']:,} events")
        print(f"   ... and {len(level_dist) - 5} more levels")
        
        client.close()
        print(f"\n✅ Database connection closed")
        print(f"\n🎯 Dashboard ready at http://localhost:8050")
        print(f"🔧 API ready at http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    populate_database()
