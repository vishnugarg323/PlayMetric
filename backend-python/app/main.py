"""
PAIME - PlayMetric AI Metrics Engine
FastAPI Application - Main Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from datetime import datetime
from typing import Dict, List, Optional

from app.database import get_sync_database, close_connections
from app.models.churn_predictor import ChurnPredictor
from app.models.level_analyzer import LevelAnalyzer
from app.services.analytics_engine import AnalyticsEngine
from app.services.game_recommendations import GameRecommendations

# Initialize ML models and services
churn_predictor = ChurnPredictor()
level_analyzer = LevelAnalyzer()
analytics_engine = AnalyticsEngine()
recommendation_engine = GameRecommendations()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 PAIME - PlayMetric AI Metrics Engine starting...")
    print("📊 Initializing AI models...")
    
    # Try to load pre-trained churn model
    try:
        if churn_predictor.load_model('models/churn_model.pkl'):
            print("✓ Loaded pre-trained churn prediction model")
        else:
            print("⚠ No pre-trained model found, using rule-based churn prediction")
    except Exception as e:
        print(f"⚠ Could not load churn model: {e}")
    
    print("✓ PAIME is ready!")
    
    yield
    
    # Shutdown
    print("Shutting down PAIME...")
    close_connections()


# Initialize FastAPI app
app = FastAPI(
    title="PAIME - PlayMetric AI Metrics Engine",
    description="""
    **AI-Powered Game Analytics Platform**
    
    PAIME provides comprehensive game analytics with machine learning insights:
    - 🤖 AI-powered churn prediction
    - 📊 Real-time analytics dashboard
    - 🎮 Level difficulty analysis
    - 💡 Actionable game improvement recommendations
    - 📈 User segmentation and behavior analysis
    
    Perfect for game developers who want to understand their players and improve their games!
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "PAIME - PlayMetric AI Metrics Engine",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "models": {
            "churn_predictor": "active" if churn_predictor.is_trained else "rule-based",
            "level_analyzer": "active",
            "analytics_engine": "active",
            "recommendation_engine": "active"
        }
    }


# Analytics Overview
@app.get("/analytics/overview", tags=["Analytics"])
async def get_analytics_overview():
    """
    Get comprehensive analytics overview
    
    Returns:
    - User metrics (DAU, MAU, retention)
    - Session analytics
    - Level statistics
    - Revenue metrics
    - Platform distribution
    """
    try:
        db = get_sync_database()
        
        # Fetch all data
        users = list(db.users.find())
        game_events = list(db.game_events.find())
        level_events = list(db.level_events.find())
        economy_events = list(db.economy_events.find())
        mission_events = list(db.mission_events.find())
        ads_events = list(db.ads_events.find())
        ui_events = list(db.ui_interaction_events.find())
        
        all_events = (
            game_events + level_events + economy_events + 
            mission_events + ads_events + ui_events
        )
        
        # Generate overview
        overview = analytics_engine.get_overview_metrics(
            users,
            all_events,
            game_events,
            level_events,
            economy_events
        )
        
        return overview
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating overview: {str(e)}")


# Churn Analysis
@app.get("/analytics/churn", tags=["AI Predictions"])
async def get_churn_analysis(limit: int = 100):
    """
    Get churn risk analysis for all users
    
    Parameters:
    - limit: Maximum number of users to analyze (default: 100)
    
    Returns:
    - Churn predictions for each user
    - Risk distribution
    - At-risk user count
    """
    try:
        db = get_sync_database()
        
        # Get users and their events
        users = list(db.users.find().limit(limit))
        
        churn_results = []
        risk_distribution = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        
        for user in users:
            user_id = user.get('userId')
            
            # Get recent events for this user (last 30 days)
            user_events = list(db.game_events.find(
                {'globalParams.userId': user_id}
            ).limit(100))
            
            level_events = list(db.level_events.find(
                {'globalParams.userId': user_id}
            ).limit(100))
            
            economy_events = list(db.economy_events.find(
                {'globalParams.userId': user_id}
            ).limit(100))
            
            all_user_events = user_events + level_events + economy_events
            
            # Predict churn
            prediction = churn_predictor.predict_churn_risk(user, all_user_events)
            
            churn_results.append({
                'user_id': user_id,
                'platform': user.get('platform', 'unknown'),
                'total_sessions': user.get('totalSessions', 0),
                'last_seen': user.get('lastSeen'),
                **prediction
            })
            
            # Update distribution
            risk_level = prediction['churn_risk']
            risk_distribution[risk_level] += 1
        
        # Sort by churn probability
        churn_results.sort(key=lambda x: x['churn_probability'], reverse=True)
        
        return {
            'total_users_analyzed': len(users),
            'risk_distribution': risk_distribution,
            'at_risk_count': risk_distribution['high'] + risk_distribution['critical'],
            'churn_predictions': churn_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in churn analysis: {str(e)}")


# Level Analysis
@app.get("/analytics/levels", tags=["Analytics"])
async def get_level_analysis():
    """
    Comprehensive level difficulty and performance analysis
    
    Returns:
    - Level statistics (completion rates, difficulty scores)
    - Drop-off levels (where players quit)
    - Bottleneck levels (high traffic, low completion)
    - Level progression funnel
    - Time analysis per level
    """
    try:
        db = get_sync_database()
        
        # Get all level events
        level_events = list(db.level_events.find())
        
        if not level_events:
            return {
                'message': 'No level data available yet',
                'level_stats': {},
                'drop_off_levels': [],
                'bottleneck_levels': []
            }
        
        # Analyze levels
        analysis = level_analyzer.analyze_all_levels(level_events)
        
        # Get progression funnel
        funnel = level_analyzer.get_level_progression_funnel(level_events)
        
        # Get time analysis
        time_analysis = level_analyzer.get_level_time_analysis(level_events)
        
        return {
            **analysis,
            'level_progression_funnel': funnel,
            'time_analysis': time_analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in level analysis: {str(e)}")


# User Segments
@app.get("/analytics/users/segments", tags=["Analytics"])
async def get_user_segments():
    """
    Get user segmentation analysis
    
    Returns:
    - Whale users (high spenders)
    - Engaged users (high activity)
    - Casual users (low activity)
    - At-risk users (declining activity)
    - New users (recently joined)
    - Dormant users (inactive)
    """
    try:
        db = get_sync_database()
        
        users = list(db.users.find())
        
        # Get all events for segmentation
        all_events = []
        for collection_name in ['game_events', 'level_events', 'economy_events', 
                                'mission_events', 'ads_events', 'ui_interaction_events']:
            all_events.extend(list(db[collection_name].find()))
        
        segments = analytics_engine.get_user_segments(users, all_events)
        
        return {
            'total_users': len(users),
            'segments': segments,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in user segmentation: {str(e)}")


# AI Recommendations
@app.get("/analytics/recommendations", tags=["AI Predictions"])
async def get_game_recommendations():
    """
    Get AI-powered game improvement recommendations
    
    Returns:
    - Critical issues (urgent fixes needed)
    - High priority improvements
    - Medium priority suggestions
    - Low priority optimizations
    - Positive insights (what's working well)
    """
    try:
        db = get_sync_database()
        
        # Get all necessary data
        users = list(db.users.find())
        game_events = list(db.game_events.find())
        level_events = list(db.level_events.find())
        economy_events = list(db.economy_events.find())
        
        all_events = game_events + level_events + economy_events
        
        # Generate overview metrics
        overview = analytics_engine.get_overview_metrics(
            users, all_events, game_events, level_events, economy_events
        )
        
        # Analyze levels
        level_analysis = level_analyzer.analyze_all_levels(level_events)
        
        # Get user segments
        user_segments = analytics_engine.get_user_segments(users, all_events)
        
        # Get churn analysis for top users
        churn_analysis = []
        for user in users[:50]:  # Analyze top 50 users
            user_events = [e for e in all_events 
                          if e.get('globalParams', {}).get('userId') == user.get('userId')]
            prediction = churn_predictor.predict_churn_risk(user, user_events)
            churn_analysis.append({
                'user_id': user.get('userId'),
                'churn_risk': prediction['churn_risk'],
                'churn_probability': prediction['churn_probability']
            })
        
        # Generate recommendations
        recommendations = recommendation_engine.generate_comprehensive_recommendations(
            overview,
            level_analysis,
            churn_analysis,
            user_segments
        )
        
        # Add summary
        recommendations['summary'] = {
            'critical_issues': len(recommendations['critical']),
            'high_priority_items': len(recommendations['high_priority']),
            'medium_priority_items': len(recommendations['medium_priority']),
            'positive_insights': len(recommendations['positive_insights']),
            'total_recommendations': (
                len(recommendations['critical']) +
                len(recommendations['high_priority']) +
                len(recommendations['medium_priority']) +
                len(recommendations['low_priority'])
            )
        }
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


# Specific User Analysis
@app.get("/analytics/users/{user_id}", tags=["Analytics"])
async def get_user_analysis(user_id: str):
    """
    Get detailed analysis for a specific user
    
    Returns:
    - User profile
    - Activity history
    - Churn risk
    - Level progress
    - Spending behavior
    """
    try:
        db = get_sync_database()
        
        # Get user
        user = db.users.find_one({'userId': user_id})
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        
        # Get all events for this user
        user_events = {
            'game_events': list(db.game_events.find({'globalParams.userId': user_id})),
            'level_events': list(db.level_events.find({'globalParams.userId': user_id})),
            'economy_events': list(db.economy_events.find({'globalParams.userId': user_id})),
            'mission_events': list(db.mission_events.find({'globalParams.userId': user_id})),
            'ads_events': list(db.ads_events.find({'globalParams.userId': user_id})),
            'ui_events': list(db.ui_interaction_events.find({'globalParams.userId': user_id}))
        }
        
        all_user_events = []
        for events in user_events.values():
            all_user_events.extend(events)
        
        # Churn prediction
        churn_prediction = churn_predictor.predict_churn_risk(user, all_user_events)
        
        # Level progress
        level_events = user_events['level_events']
        levels_completed = len([e for e in level_events if e.get('completed', False)])
        max_level = max([e.get('levelNumber', 0) for e in level_events], default=0)
        
        # Spending
        total_spent = sum([
            e.get('realMoneyValue', 0) 
            for e in user_events['economy_events']
        ])
        
        # Remove MongoDB _id fields for JSON serialization
        for event_list in user_events.values():
            for event in event_list:
                if '_id' in event:
                    del event['_id']
        
        if '_id' in user:
            del user['_id']
        
        return {
            'user': user,
            'churn_analysis': churn_prediction,
            'level_progress': {
                'levels_completed': levels_completed,
                'max_level_reached': max_level,
                'total_attempts': len(level_events)
            },
            'spending': {
                'total_spent': total_spent,
                'total_transactions': len([
                    e for e in user_events['economy_events'] 
                    if e.get('realMoneyValue', 0) > 0
                ])
            },
            'event_counts': {
                event_type: len(events)
                for event_type, events in user_events.items()
            },
            'recent_events': sorted(
                all_user_events,
                key=lambda e: e.get('globalParams', {}).get('timestamp', ''),
                reverse=True
            )[:20]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing user: {str(e)}")


# Data Statistics
@app.get("/analytics/stats", tags=["Analytics"])
async def get_data_statistics():
    """
    Get raw data statistics
    
    Returns counts for all collections and basic stats
    """
    try:
        db = get_sync_database()
        
        stats = {
            'users': db.users.count_documents({}),
            'game_events': db.game_events.count_documents({}),
            'level_events': db.level_events.count_documents({}),
            'economy_events': db.economy_events.count_documents({}),
            'mission_events': db.mission_events.count_documents({}),
            'ads_events': db.ads_events.count_documents({}),
            'ui_interaction_events': db.ui_interaction_events.count_documents({}),
        }
        
        stats['total_events'] = sum([
            stats['game_events'],
            stats['level_events'],
            stats['economy_events'],
            stats['mission_events'],
            stats['ads_events'],
            stats['ui_interaction_events']
        ])
        
        return {
            'timestamp': datetime.now().isoformat(),
            'statistics': stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to PAIME - PlayMetric AI Metrics Engine",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health",
        "dashboard": "http://localhost:8050"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
