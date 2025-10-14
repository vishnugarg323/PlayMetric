"""
Churn Prediction Model using Random Forest
Predicts user churn risk based on behavioral patterns
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pickle
import os


class ChurnPredictor:
    """
    ML model to predict user churn probability
    
    Features used:
    - Days since last session
    - Total sessions
    - Average session duration
    - Level completion rate
    - Total events
    - Days since registration
    - Purchase history
    - Engagement trend (declining/stable/growing)
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=20,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'days_since_last_session',
            'total_sessions',
            'avg_session_duration',
            'level_completion_rate',
            'total_events',
            'days_since_registration',
            'total_purchases',
            'purchase_amount',
            'engagement_trend',
            'recent_activity_score'
        ]
    
    def extract_features(self, user_data: Dict, events_data: List[Dict]) -> np.ndarray:
        """
        Extract ML features from user and event data
        
        Args:
            user_data: User profile from MongoDB
            events_data: List of recent events for the user
            
        Returns:
            Feature vector as numpy array
        """
        now = datetime.now()
        
        # Calculate days since last session
        last_seen = user_data.get('lastSeen', now)
        if isinstance(last_seen, str):
            last_seen = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
        days_since_last = (now - last_seen).days
        
        # Calculate days since registration
        first_seen = user_data.get('firstSeen', now)
        if isinstance(first_seen, str):
            first_seen = datetime.fromisoformat(first_seen.replace('Z', '+00:00'))
        days_since_registration = (now - first_seen).days + 1
        
        # Basic metrics
        total_sessions = user_data.get('totalSessions', 0)
        total_events = user_data.get('totalEvents', 0)
        
        # Calculate average session duration from recent events
        session_durations = [
            e.get('globalParams', {}).get('sessionDuration', 0) 
            for e in events_data 
            if e.get('globalParams', {}).get('sessionDuration')
        ]
        avg_session_duration = np.mean(session_durations) if session_durations else 0
        
        # Calculate level completion rate
        level_events = [e for e in events_data if e.get('eventType', '').startswith('LEVEL_')]
        level_completes = len([e for e in level_events if e.get('completed', False)])
        level_completion_rate = level_completes / len(level_events) if level_events else 0
        
        # Purchase metrics
        purchase_events = [e for e in events_data if e.get('eventType', '').startswith('ECONOMY_')]
        total_purchases = len(purchase_events)
        purchase_amount = sum([
            e.get('realMoneyValue', 0) 
            for e in purchase_events 
            if e.get('realMoneyValue')
        ])
        
        # Engagement trend (last 7 days vs previous 7 days)
        seven_days_ago = now - timedelta(days=7)
        fourteen_days_ago = now - timedelta(days=14)
        
        recent_events = [e for e in events_data if self._parse_timestamp(e) > seven_days_ago]
        previous_events = [
            e for e in events_data 
            if fourteen_days_ago < self._parse_timestamp(e) <= seven_days_ago
        ]
        
        recent_count = len(recent_events)
        previous_count = len(previous_events)
        
        if previous_count > 0:
            engagement_trend = (recent_count - previous_count) / previous_count
        else:
            engagement_trend = 0 if recent_count == 0 else 1
        
        # Recent activity score (weighted by recency)
        recent_activity_score = self._calculate_activity_score(events_data, now)
        
        # Compile features
        features = np.array([
            days_since_last,
            total_sessions,
            avg_session_duration / 1000,  # Convert to seconds
            level_completion_rate,
            total_events,
            days_since_registration,
            total_purchases,
            purchase_amount,
            engagement_trend,
            recent_activity_score
        ])
        
        return features.reshape(1, -1)
    
    def _parse_timestamp(self, event: Dict) -> datetime:
        """Parse timestamp from event"""
        timestamp = event.get('globalParams', {}).get('timestamp', datetime.now())
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return timestamp
    
    def _calculate_activity_score(self, events: List[Dict], now: datetime) -> float:
        """Calculate activity score with exponential decay"""
        score = 0.0
        for event in events:
            timestamp = self._parse_timestamp(event)
            days_ago = (now - timestamp).days
            # Exponential decay: weight = e^(-days/7)
            weight = np.exp(-days_ago / 7)
            score += weight
        return score
    
    def train(self, training_data: List[Tuple[Dict, List[Dict], bool]]):
        """
        Train the churn prediction model
        
        Args:
            training_data: List of (user_data, events_data, is_churned) tuples
        """
        X = []
        y = []
        
        for user_data, events_data, is_churned in training_data:
            features = self.extract_features(user_data, events_data)
            X.append(features[0])
            y.append(1 if is_churned else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        return self.model.score(X_scaled, y)
    
    def predict_churn_risk(self, user_data: Dict, events_data: List[Dict]) -> Dict:
        """
        Predict churn probability for a user
        
        Returns:
            {
                'churn_probability': float,
                'churn_risk': str (low/medium/high/critical),
                'risk_factors': List[str],
                'recommendations': List[str]
            }
        """
        if not self.is_trained:
            # Use rule-based system if model not trained
            return self._rule_based_prediction(user_data, events_data)
        
        features = self.extract_features(user_data, events_data)
        features_scaled = self.scaler.transform(features)
        
        churn_prob = self.model.predict_proba(features_scaled)[0][1]
        
        # Determine risk level
        if churn_prob < 0.25:
            risk_level = "low"
        elif churn_prob < 0.5:
            risk_level = "medium"
        elif churn_prob < 0.75:
            risk_level = "high"
        else:
            risk_level = "critical"
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(features[0], user_data, events_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_factors, user_data)
        
        return {
            'churn_probability': round(churn_prob, 3),
            'churn_risk': risk_level,
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'confidence': round(self.model.predict_proba(features_scaled)[0].max(), 3)
        }
    
    def _rule_based_prediction(self, user_data: Dict, events_data: List[Dict]) -> Dict:
        """Fallback rule-based churn prediction"""
        now = datetime.now()
        last_seen = user_data.get('lastSeen', now)
        if isinstance(last_seen, str):
            last_seen = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
        
        days_inactive = (now - last_seen).days
        total_sessions = user_data.get('totalSessions', 0)
        
        # Simple rules
        if days_inactive > 14:
            churn_prob = 0.9
        elif days_inactive > 7:
            churn_prob = 0.7
        elif days_inactive > 3:
            churn_prob = 0.4
        elif total_sessions < 3:
            churn_prob = 0.5
        else:
            churn_prob = 0.2
        
        risk_factors = []
        if days_inactive > 7:
            risk_factors.append(f"Inactive for {days_inactive} days")
        if total_sessions < 5:
            risk_factors.append("Low engagement (few sessions)")
        
        return {
            'churn_probability': churn_prob,
            'churn_risk': "high" if churn_prob > 0.6 else "medium" if churn_prob > 0.3 else "low",
            'risk_factors': risk_factors or ["No significant risk factors"],
            'recommendations': self._generate_recommendations(risk_factors, user_data),
            'confidence': 0.7
        }
    
    def _identify_risk_factors(self, features: np.ndarray, user_data: Dict, events_data: List[Dict]) -> List[str]:
        """Identify specific risk factors for the user"""
        factors = []
        
        days_since_last = features[0]
        total_sessions = features[1]
        level_completion_rate = features[3]
        engagement_trend = features[8]
        total_purchases = features[6]
        
        if days_since_last > 7:
            factors.append(f"No activity for {int(days_since_last)} days")
        elif days_since_last > 3:
            factors.append(f"Reduced activity ({int(days_since_last)} days since last session)")
        
        if total_sessions < 5:
            factors.append("Low overall engagement")
        
        if level_completion_rate < 0.3:
            factors.append(f"Low level completion rate ({level_completion_rate:.1%})")
        
        if engagement_trend < -0.3:
            factors.append(f"Declining engagement (down {abs(engagement_trend):.1%})")
        
        if total_purchases == 0 and total_sessions > 10:
            factors.append("No purchases despite active play")
        
        return factors or ["No significant risk factors detected"]
    
    def _generate_recommendations(self, risk_factors: List[str], user_data: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        risk_text = " ".join(risk_factors)
        
        if "Inactive" in risk_text or "Reduced activity" in risk_text:
            recommendations.append("Send re-engagement notification with special reward")
            recommendations.append("Offer limited-time bonus or exclusive content")
        
        if "Low level completion" in risk_text:
            recommendations.append("Provide hints or skip option for difficult levels")
            recommendations.append("Adjust level difficulty based on player skill")
        
        if "Declining engagement" in risk_text:
            recommendations.append("Introduce new content or game modes")
            recommendations.append("Create time-limited events to boost engagement")
        
        if "No purchases" in risk_text:
            recommendations.append("Offer first-purchase discount or special offer")
            recommendations.append("Show value of premium features through gameplay")
        
        if "Low overall engagement" in risk_text:
            recommendations.append("Improve onboarding experience")
            recommendations.append("Add social features or multiplayer modes")
        
        return recommendations or ["Continue monitoring player behavior"]
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': self.is_trained,
            'feature_names': self.feature_names
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.is_trained = model_data['is_trained']
            self.feature_names = model_data['feature_names']
            return True
        return False
