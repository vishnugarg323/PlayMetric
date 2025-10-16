"""
ULTIMATE Data Population Script for PAIME
Generates 100,000+ realistic game analytics events with meaningful user names
Covers all scenarios: ads, monetization, level analysis, churn, and more
"""
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
import uuid
from collections import defaultdict

# MongoDB Configuration
MONGODB_URI = "mongodb://mongo:gSFyjoeBNGrWpElewAfFLzloUYmSyqRm@gondola.proxy.rlwy.net:21458/playmetric?authSource=admin"
DATABASE_NAME = "playmetric"

# Game Configuration
GAME_NAME = "Shadow Quest: Legends"
GAME_ID = "shadow_quest_legends"
NUM_USERS = 10
TARGET_GAME_EVENTS = 10000
TARGET_LEVEL_EVENTS = 100000
NUM_LEVELS = 30
PLATFORMS = ['ANDROID', 'IOS', 'WEB']
CURRENCIES = ['COINS', 'GEMS', 'ENERGY', 'GOLD']
AD_TYPES = ['REWARDED', 'INTERSTITIAL', 'BANNER']

# Realistic player names
FIRST_NAMES = ['Alex', 'Jordan', 'Morgan', 'Casey', 'Riley', 'Cameron', 'Taylor', 'Dakota', 'Avery', 'Quinn']
LAST_NAMES = ['Storm', 'Shadow', 'Phoenix', 'Blade', 'Hunter', 'Knight', 'Raven', 'Wolf', 'Dragon', 'Falcon']

# User behavior archetypes
USER_ARCHETYPES = {
    'whale': {
        'sessions_range': (150, 250),
        'purchase_probability': 0.25,
        'churn_risk': 0.05,
        'skill_level': 0.9,
        'retention': 0.95
    },
    'engaged': {
        'sessions_range': (100, 180),
        'purchase_probability': 0.08,
        'churn_risk': 0.15,
        'skill_level': 0.75,
        'retention': 0.85
    },
    'casual': {
        'sessions_range': (40, 100),
        'purchase_probability': 0.03,
        'churn_risk': 0.35,
        'skill_level': 0.6,
        'retention': 0.65
    },
    'at_risk': {
        'sessions_range': (15, 40),
        'purchase_probability': 0.01,
        'churn_risk': 0.70,
        'skill_level': 0.45,
        'retention': 0.35
    },
    'dormant': {
        'sessions_range': (5, 15),
        'purchase_probability': 0.005,
        'churn_risk': 0.95,
        'skill_level': 0.3,
        'retention': 0.10
    }
}

def generate_username(index):
    """Generate meaningful player username"""
    first = FIRST_NAMES[index % len(FIRST_NAMES)]
    last = LAST_NAMES[(index // len(FIRST_NAMES)) % len(LAST_NAMES)]
    return f"{first}{last}{random.randint(10, 99)}"

def generate_user_profile(user_index, start_date):
    """Generate realistic user profile with meaningful name"""
    archetype = random.choices(
        ['whale', 'engaged', 'casual', 'at_risk', 'dormant'],
        weights=[0.05, 0.20, 0.35, 0.25, 0.15]
    )[0]
    
    username = generate_username(user_index)
    user_id = f"{username.lower()}_uid"
    platform = random.choice(PLATFORMS)
    registration_date = start_date + timedelta(days=random.randint(0, 28))
    
    arch_config = USER_ARCHETYPES[archetype]
    total_sessions = random.randint(*arch_config['sessions_range'])
    
    # Calculate last seen based on archetype
    if archetype == 'dormant':
        last_seen = datetime.now() - timedelta(days=random.randint(20, 35))
    elif archetype == 'at_risk':
        last_seen = datetime.now() - timedelta(days=random.randint(7, 15))
    elif archetype == 'casual':
        last_seen = datetime.now() - timedelta(days=random.randint(1, 5))
    else:
        last_seen = datetime.now() - timedelta(hours=random.randint(1, 24))
    
    return {
        'userId': user_id,
        'username': username,
        'displayName': f"{username}",
        'email': f"{username.lower()}@gamers.com",
        'platform': platform,
        'registrationDate': registration_date,
        'lastSeen': last_seen,
        'archetype': archetype,
        'totalSessions': total_sessions,
        'deviceId': f"device_{uuid.uuid4().hex[:12]}",
        'deviceModel': random.choice(['Samsung Galaxy S23', 'iPhone 15 Pro', 'Pixel 8', 'OnePlus 11', 'iPad Pro']),
        'osVersion': random.choice(['Android 14', 'iOS 17', 'Android 13', 'iOS 16', 'Web']),
        'country': random.choice(['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP', 'BR', 'IN', 'KR']),
        'skillLevel': arch_config['skill_level'],
        'totalEvents': 0,
        'totalPurchases': 0,
        'totalSpent': 0.0,
        'maxLevelReached': 0,
        'completedLevels': 0,
        'adRevenue': 0.0,
        'totalPlaytime': 0
    }

def generate_global_params(user, session_id, timestamp):
    """Generate global event parameters"""
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
            'appVersion': '2.1.5'
        }
    }

def calculate_level_difficulty(level_num):
    """Calculate difficulty curve for levels"""
    # Easy early levels, exponential difficulty growth
    base_difficulty = 1.0
    if level_num <= 3:
        return base_difficulty * level_num * 0.5
    elif level_num <= 10:
        return base_difficulty * level_num * 0.8
    elif level_num <= 20:
        return base_difficulty * level_num * 1.2
    else:
        return base_difficulty * level_num * 1.5

def generate_level_event(event_type, level_num, global_params, user):
    """Generate comprehensive level event"""
    difficulty_mult = calculate_level_difficulty(level_num)
    skill = user['skillLevel']
    
    event = {
        'globalParams': global_params,
        'eventType': event_type,
        'gameId': GAME_ID,
        'levelId': f"level_{level_num}",
        'levelNumber': level_num,
        'timestamp': global_params['timestamp']
    }
    
    if event_type == 'LEVEL_START':
        event['attemptNumber'] = random.randint(1, max(1, int(4 * difficulty_mult / skill)))
        
    elif event_type == 'LEVEL_COMPLETE':
        # Success influenced by skill and difficulty
        success_rate = skill / difficulty_mult
        perfect = success_rate > 1.5 and random.random() < 0.15
        
        base_score = 1000 * level_num
        score = int(base_score * skill * random.uniform(0.8, 1.2))
        
        stars = 3 if success_rate > 1.3 else (2 if success_rate > 0.9 else 1)
        time_taken = int((60 + level_num * 10) / skill + random.uniform(-20, 20))
        
        event.update({
            'completed': True,
            'score': score,
            'starsEarned': stars,
            'perfectCompletion': perfect,
            'levelDuration': time_taken,
            'hintsUsed': 0 if skill > 0.7 else random.randint(0, 3),
            'powerupsUsed': random.randint(0, int(3 / skill)),
            'itemsCollected': random.randint(int(10 * skill), int(50 * skill)),
            'enemiesDefeated': random.randint(int(5 * skill), int(30 * skill)),
            'damagesTaken': random.randint(0, int(15 / skill))
        })
        
    elif event_type == 'LEVEL_FAILED':
        fail_score = int(500 * level_num * skill * random.uniform(0.3, 0.7))
        fail_reasons = ['TIME_OUT', 'HEALTH_DEPLETED', 'OBJECTIVE_FAILED', 'ENEMY_DEFEATED_PLAYER']
        
        event.update({
            'completed': False,
            'score': fail_score,
            'failReason': random.choice(fail_reasons),
            'levelDuration': int((40 + level_num * 8) / skill),
            'damagesTaken': random.randint(int(5 / skill), int(20 / skill)),
            'checkpointReached': f"checkpoint_{random.randint(1, 3)}" if random.random() > 0.5 else None
        })
    
    return event

def generate_economy_event(event_type, global_params, user):
    """Generate realistic economy event"""
    currency = random.choice(CURRENCIES)
    archetype = user['archetype']
    arch_config = USER_ARCHETYPES[archetype]
    
    # Amount based on user type
    if archetype == 'whale':
        amount = random.randint(200, 5000)
    elif archetype == 'engaged':
        amount = random.randint(100, 2000)
    else:
        amount = random.randint(20, 800)
    
    event = {
        'globalParams': global_params,
        'eventType': event_type,
        'currencyType': currency,
        'amount': amount,
        'balanceAfter': random.randint(amount, amount + 10000),
        'timestamp': global_params['timestamp']
    }
    
    if event_type == 'ECONOMY_PURCHASE':
        # Real money purchases for monetization analysis
        if random.random() < arch_config['purchase_probability']:
            price = random.choices(
                [0.99, 1.99, 4.99, 9.99, 19.99, 49.99, 99.99],
                weights=[0.30, 0.25, 0.20, 0.15, 0.07, 0.02, 0.01]
            )[0]
            event['priceInRealMoney'] = price
            event['transactionType'] = 'IAP'
        else:
            event['priceInRealMoney'] = None
            event['transactionType'] = 'IN_GAME'
        
        item_types = ['POWER_UP_PACK', 'COIN_BUNDLE', 'GEM_BUNDLE', 'ENERGY_REFILL', 'PREMIUM_ITEM', 'BOOST_PACK', 'SPECIAL_WEAPON']
        event.update({
            'itemId': f"item_{random.randint(100, 999)}",
            'itemName': random.choice(item_types).replace('_', ' ').title(),
            'itemCategory': random.choice(['CONSUMABLE', 'PERMANENT', 'CURRENCY']),
            'transactionId': str(uuid.uuid4())
        })
        
    elif event_type == 'ECONOMY_EARN':
        event['source'] = random.choice([
            'LEVEL_COMPLETE', 'DAILY_REWARD', 'ACHIEVEMENT_UNLOCKED', 
            'AD_REWARD', 'MISSION_COMPLETE', 'LOGIN_BONUS', 'EVENT_REWARD'
        ])
        
    elif event_type == 'ECONOMY_SPEND':
        event['spentOn'] = random.choice([
            'POWER_UP', 'UNLOCK_LEVEL', 'BOOST', 'CONTINUE_GAME', 
            'COSMETIC_ITEM', 'CHARACTER_UPGRADE', 'WEAPON_UPGRADE'
        ])
    
    return event

def generate_ads_event(global_params, user):
    """Generate detailed ads event for monetization analysis"""
    ad_type = random.choice(AD_TYPES)
    ad_networks = ['AdMob', 'Unity Ads', 'Facebook Audience', 'IronSource', 'AppLovin']
    ad_placements = ['LEVEL_START', 'LEVEL_COMPLETE', 'GAME_OVER', 'REWARD_GATE', 'MAIN_MENU']
    
    event = {
        'globalParams': global_params,
        'eventType': 'ADS_IMPRESSION',
        'adType': ad_type,
        'adNetwork': random.choice(ad_networks),
        'adPlacement': random.choice(ad_placements),
        'adFormat': random.choice(['VIDEO', 'STATIC', 'PLAYABLE']),
        'timestamp': global_params['timestamp']
    }
    
    # Revenue calculation
    if ad_type == 'REWARDED':
        completion_rate = 0.75 if user['archetype'] in ['engaged', 'whale'] else 0.55
        completed = random.random() < completion_rate
        event.update({
            'completed': completed,
            'rewardType': random.choice(CURRENCIES) if completed else None,
            'rewardAmount': random.randint(50, 200) if completed else 0,
            'adDuration': random.randint(15, 30),
            'skipped': not completed
        })
        # Revenue per rewarded ad
        event['revenue'] = round(random.uniform(0.01, 0.05), 4) if completed else 0
        
    elif ad_type == 'INTERSTITIAL':
        event['adDuration'] = random.randint(5, 15)
        event['skipped'] = random.random() < 0.20
        event['revenue'] = round(random.uniform(0.005, 0.02), 4)
        
    elif ad_type == 'BANNER':
        event['revenue'] = round(random.uniform(0.001, 0.005), 4)
    
    event['clicked'] = random.random() < 0.05  # 5% CTR
    
    return event

def generate_mission_event(event_type, global_params, user):
    """Generate mission event"""
    mission_types = ['DAILY', 'WEEKLY', 'ACHIEVEMENT', 'SPECIAL_EVENT']
    mission_goals = [
        'Complete 5 levels', 'Defeat 50 enemies', 'Collect 1000 coins',
        'Win 3 battles in a row', 'Use 10 power-ups', 'Play for 30 minutes',
        'Reach level 10', 'Earn 3 stars on 5 levels', 'Watch 5 ads'
    ]
    
    mission_id = random.randint(1, 100)
    event = {
        'globalParams': global_params,
        'eventType': event_type,
        'missionType': random.choice(mission_types),
        'missionId': mission_id,
        'missionName': random.choice(mission_goals),
        'timestamp': global_params['timestamp']
    }
    
    if event_type == 'MISSION_COMPLETE':
        reward_amount = random.randint(100, 1000)
        event.update({
            'completed': True,
            'rewardType': random.choice(CURRENCIES),
            'rewardAmount': reward_amount,
            'rewardClaimed': random.random() < 0.9,  # 90% claim rate
            'missionDuration': random.randint(300, 3600)
        })
    else:  # MISSION_START
        event['progressPercentage'] = random.randint(0, 30)
    
    return event

def generate_ui_event(global_params):
    """Generate UI interaction event"""
    screens = ['MAIN_MENU', 'LEVEL_SELECT', 'SHOP', 'SETTINGS', 'INVENTORY', 'LEADERBOARD', 'PROFILE']
    elements = ['BUTTON_PLAY', 'BUTTON_SHOP', 'BUTTON_SETTINGS', 'SLIDER_VOLUME', 
                'TOGGLE_MUSIC', 'BUTTON_SHARE', 'TAB_LEVELS', 'POPUP_OFFER']
    
    return {
        'globalParams': global_params,
        'eventType': 'UI_INTERACTION',
        'screenName': random.choice(screens),
        'elementId': f"ui_{random.randint(100, 999)}",
        'elementName': random.choice(elements),
        'elementType': random.choice(['BUTTON', 'TOGGLE', 'SLIDER', 'TAB']),
        'action': random.choice(['CLICK', 'SWIPE', 'LONG_PRESS', 'DRAG']),
        'timestamp': global_params['timestamp']
    }

def generate_game_event(event_type, global_params, session_duration=None):
    """Generate game session event"""
    event = {
        'globalParams': global_params,
        'eventType': event_type,
        'gameId': GAME_ID,
        'timestamp': global_params['timestamp']
    }
    
    if event_type == 'GAME_END' and session_duration:
        event['sessionDuration'] = session_duration
        event['score'] = random.randint(1000, 50000)
    
    return event

def populate_ultimate_database():
    """Populate database with comprehensive realistic data"""
    print("=" * 70)
    print("🎮 PAIME ULTIMATE DATA POPULATION")
    print("=" * 70)
    print(f"\n📊 Target Configuration:")
    print(f"   • Game: {GAME_NAME}")
    print(f"   • Users: {NUM_USERS} with meaningful names")
    print(f"   • Target Game Events: {TARGET_GAME_EVENTS:,}")
    print(f"   • Target Level Events: {TARGET_LEVEL_EVENTS:,}")
    print(f"   • Levels: {NUM_LEVELS}")
    print(f"   • Scenarios: Ads, Monetization, Churn, Level Analysis\n")
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=15000)
        db = client[DATABASE_NAME]
        client.server_info()
        print("✅ Connected to Railway MongoDB\n")
        
        # Clear collections
        print("🧹 Clearing existing data...")
        collections = ['users', 'level_events', 'game_events', 'economy_events',
                      'mission_events', 'ads_events', 'ui_interaction_events']
        for coll in collections:
            db[coll].delete_many({})
        print("✅ Database cleared\n")
        
        # Generate users
        start_date = datetime.now() - timedelta(days=35)
        users = [generate_user_profile(i, start_date) for i in range(NUM_USERS)]
        
        print("👥 Generated Users:")
        for user in users:
            print(f"   • {user['username']:20s} ({user['archetype']:8s}) - {user['platform']}")
        print()
        
        # Event collections
        all_events = {
            'level': [],
            'game': [],
            'economy': [],
            'mission': [],
            'ads': [],
            'ui': []
        }
        
        # User statistics
        user_stats = defaultdict(lambda: {
            'total_events': 0,
            'total_purchases': 0,
            'total_spent': 0.0,
            'max_level': 0,
            'completed_levels': set(),
            'ad_revenue': 0.0,
            'playtime': 0
        })
        
        # Generate events
        print("⚙️  Generating events for each user...\n")
        
        for idx, user in enumerate(users, 1):
            user_id = user['userId']
            archetype = user['archetype']
            arch_config = USER_ARCHETYPES[archetype]
            
            print(f"[{idx}/{NUM_USERS}] Processing {user['username']} ({archetype})...")
            
            num_sessions = user['totalSessions']
            current_level = 1
            max_level = 1
            current_date = user['registrationDate']
            
            # Calculate events per user to hit target
            level_events_per_user = TARGET_LEVEL_EVENTS // NUM_USERS
            game_events_per_user = TARGET_GAME_EVENTS // NUM_USERS
            
            events_per_session = max(10, level_events_per_user // num_sessions)
            
            for session_num in range(num_sessions):
                session_id = f"session_{uuid.uuid4().hex[:8]}"
                
                # Time progression
                if archetype == 'dormant':
                    current_date += timedelta(days=random.randint(2, 6))
                elif archetype == 'at_risk':
                    current_date += timedelta(days=random.randint(1, 4))
                else:
                    current_date += timedelta(hours=random.randint(2, 48))
                
                if current_date > datetime.now():
                    break
                
                session_start_time = current_date
                session_duration = random.randint(180, 3600)
                
                # Session start
                gp = generate_global_params(user, session_id, current_date)
                all_events['game'].append(generate_game_event('GAME_START', gp))
                
                # Events within session
                for event_idx in range(events_per_session):
                    event_time = current_date + timedelta(seconds=random.randint(0, session_duration))
                    gp = generate_global_params(user, session_id, event_time)
                    
                    # Event distribution focused on level events
                    event_type = random.choices(
                        ['level', 'economy', 'ads', 'mission', 'ui'],
                        weights=[0.65, 0.15, 0.10, 0.06, 0.04]
                    )[0]
                    
                    if event_type == 'level':
                        # Level event flow
                        level_action = random.choices(
                            ['START', 'COMPLETE', 'FAILED'],
                            weights=[0.35, 0.40, 0.25]
                        )[0]
                        
                        if level_action == 'START':
                            event = generate_level_event('LEVEL_START', current_level, gp, user)
                            all_events['level'].append(event)
                            
                        elif level_action == 'COMPLETE':
                            event = generate_level_event('LEVEL_COMPLETE', current_level, gp, user)
                            all_events['level'].append(event)
                            user_stats[user_id]['completed_levels'].add(current_level)
                            
                            # Level progression
                            progress_prob = arch_config['skill_level']
                            if random.random() < progress_prob:
                                current_level = min(current_level + 1, NUM_LEVELS)
                                max_level = max(max_level, current_level)
                                
                        else:  # FAILED
                            event = generate_level_event('LEVEL_FAILED', current_level, gp, user)
                            all_events['level'].append(event)
                    
                    elif event_type == 'economy':
                        eco_action = random.choice(['ECONOMY_PURCHASE', 'ECONOMY_EARN', 'ECONOMY_SPEND'])
                        event = generate_economy_event(eco_action, gp, user)
                        all_events['economy'].append(event)
                        
                        if eco_action == 'ECONOMY_PURCHASE' and event.get('priceInRealMoney'):
                            user_stats[user_id]['total_purchases'] += 1
                            user_stats[user_id]['total_spent'] += event['priceInRealMoney']
                    
                    elif event_type == 'ads':
                        event = generate_ads_event(gp, user)
                        all_events['ads'].append(event)
                        user_stats[user_id]['ad_revenue'] += event.get('revenue', 0)
                    
                    elif event_type == 'mission':
                        mission_action = random.choice(['MISSION_START', 'MISSION_COMPLETE'])
                        event = generate_mission_event(mission_action, gp, user)
                        all_events['mission'].append(event)
                    
                    elif event_type == 'ui':
                        event = generate_ui_event(gp)
                        all_events['ui'].append(event)
                    
                    user_stats[user_id]['total_events'] += 1
                
                # Session end
                end_time = current_date + timedelta(seconds=session_duration)
                gp = generate_global_params(user, session_id, end_time)
                all_events['game'].append(generate_game_event('GAME_END', gp, session_duration))
                
                user_stats[user_id]['max_level'] = max_level
                user_stats[user_id]['playtime'] += session_duration
            
            print(f"    ✓ {user_stats[user_id]['total_events']:,} events | Level {max_level} | ${user_stats[user_id]['total_spent']:.2f}")
        
        # Update user profiles
        print("\n💾 Finalizing user profiles...")
        for user in users:
            uid = user['userId']
            stats = user_stats[uid]
            user.update({
                'totalEvents': stats['total_events'],
                'totalPurchases': stats['total_purchases'],
                'totalSpent': round(stats['total_spent'], 2),
                'maxLevelReached': stats['max_level'],
                'completedLevels': len(stats['completed_levels']),
                'adRevenue': round(stats['ad_revenue'], 2),
                'totalPlaytime': stats['playtime']
            })
        
        # Insert data
        print("\n💾 Inserting data into MongoDB...")
        
        db.users.insert_many(users)
        print(f"   ✓ Users: {len(users):,}")
        
        counts = {}
        for event_type, events in all_events.items():
            if events:
                collection = f"{event_type}_events"
                db[collection].insert_many(events)
                counts[collection] = len(events)
                print(f"   ✓ {collection}: {len(events):,}")
        
        # Final statistics
        total_events = sum(counts.values())
        total_revenue = sum(u['totalSpent'] for u in users)
        total_ad_revenue = sum(u['adRevenue'] for u in users)
        
        print("\n" + "=" * 70)
        print("🎉 DATA POPULATION COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Final Statistics:")
        print(f"   • Total Events: {total_events:,}")
        print(f"   • Level Events: {counts.get('level_events', 0):,}")
        print(f"   • Game Events: {counts.get('game_events', 0):,}")
        print(f"\n💰 Revenue:")
        print(f"   • IAP Revenue: ${total_revenue:.2f}")
        print(f"   • Ad Revenue: ${total_ad_revenue:.2f}")
        print(f"   • Total Revenue: ${(total_revenue + total_ad_revenue):.2f}")
        
        print(f"\n👥 User Distribution:")
        arch_dist = defaultdict(int)
        for u in users:
            arch_dist[u['archetype']] += 1
        for arch, count in sorted(arch_dist.items()):
            print(f"   • {arch.capitalize():10s}: {count} users")
        
        print(f"\n🎯 Next Steps:")
        print(f"   • Dashboard: http://localhost:8050")
        print(f"   • API: http://localhost:8000/analytics/overview")
        print(f"   • Java API: http://localhost:8080/swagger-ui.html")
        print("\n" + "=" * 70)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    populate_ultimate_database()
