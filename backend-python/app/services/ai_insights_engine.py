"""
Advanced AI Insights Engine
Provides comprehensive AI-powered analytics and predictions
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class AIInsightsEngine:
    """
    Advanced AI-powered analytics engine
    
    Features:
    - Predictive player behavior modeling
    - Automated anomaly detection
    - Revenue optimization suggestions
    - Level difficulty balancing
    - Player segmentation with ML
    - Trend forecasting
    - Personalized engagement strategies
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def generate_comprehensive_insights(
        self,
        users: List[Dict],
        all_events: List[Dict],
        level_events: List[Dict],
        economy_events: List[Dict],
        churn_predictions: List[Dict]
    ) -> Dict:
        """Generate all AI insights in one comprehensive analysis"""
        
        insights = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'player_behavior_analysis': self._analyze_player_behavior(users, all_events),
            'revenue_optimization': self._analyze_revenue_opportunities(economy_events, users),
            'level_balancing': self._analyze_level_balance(level_events),
            'engagement_predictions': self._predict_engagement_trends(users, all_events),
            'anomaly_detection': self._detect_anomalies(all_events, users),
            'player_segments_ml': self._ml_player_segmentation(users, all_events),
            'retention_drivers': self._identify_retention_drivers(users, all_events),
            'monetization_patterns': self._analyze_monetization_patterns(economy_events, users),
            'content_recommendations': self._generate_content_recommendations(level_events, users),
            'risk_assessment': self._assess_business_risks(churn_predictions, users, economy_events),
            'opportunity_score': self._calculate_opportunity_scores(users, all_events, economy_events)
        }
        
        # Generate executive summary
        insights['executive_summary'] = self._generate_executive_summary(insights)
        
        return insights
    
    def _analyze_player_behavior(self, users: List[Dict], events: List[Dict]) -> Dict:
        """Deep dive into player behavior patterns"""
        
        if not users or not events:
            return {}
        
        # Group events by user
        user_events = defaultdict(list)
        for event in events:
            user_id = event.get('globalParams', {}).get('userId')
            if user_id:
                user_events[user_id].append(event)
        
        # Analyze session patterns
        session_patterns = self._analyze_session_patterns(user_events)
        
        # Analyze play time patterns (peak hours)
        peak_hours = self._analyze_peak_hours(events)
        
        # Player lifecycle stages
        lifecycle_distribution = self._analyze_lifecycle_stages(users)
        
        # Engagement velocity (how fast users progress)
        engagement_velocity = self._calculate_engagement_velocity(users, user_events)
        
        return {
            'session_patterns': session_patterns,
            'peak_activity_hours': peak_hours,
            'lifecycle_distribution': lifecycle_distribution,
            'engagement_velocity': engagement_velocity,
            'key_findings': self._generate_behavior_findings(
                session_patterns, peak_hours, lifecycle_distribution
            )
        }
    
    def _analyze_session_patterns(self, user_events: Dict[str, List[Dict]]) -> Dict:
        """Analyze how users structure their gaming sessions"""
        
        session_types = {
            'marathon': 0,      # > 30 min
            'standard': 0,      # 10-30 min
            'quick': 0,         # 5-10 min
            'micro': 0          # < 5 min
        }
        
        session_durations = []
        for user_id, events in user_events.items():
            for event in events:
                duration_ms = event.get('globalParams', {}).get('sessionDuration', 0)
                if duration_ms > 0:
                    duration_min = duration_ms / 1000 / 60
                    session_durations.append(duration_min)
                    
                    if duration_min > 30:
                        session_types['marathon'] += 1
                    elif duration_min > 10:
                        session_types['standard'] += 1
                    elif duration_min > 5:
                        session_types['quick'] += 1
                    else:
                        session_types['micro'] += 1
        
        total = sum(session_types.values())
        
        return {
            'distribution': {
                k: {'count': v, 'percentage': round(v/total*100, 2) if total > 0 else 0}
                for k, v in session_types.items()
            },
            'avg_duration_minutes': round(np.mean(session_durations), 2) if session_durations else 0,
            'median_duration_minutes': round(np.median(session_durations), 2) if session_durations else 0,
            'std_dev_minutes': round(np.std(session_durations), 2) if session_durations else 0
        }
    
    def _analyze_peak_hours(self, events: List[Dict]) -> Dict:
        """Identify peak playing hours"""
        
        hourly_activity = defaultdict(int)
        
        for event in events:
            timestamp = event.get('globalParams', {}).get('timestamp')
            if timestamp:
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                hour = timestamp.hour
                hourly_activity[hour] += 1
        
        if not hourly_activity:
            return {}
        
        sorted_hours = sorted(hourly_activity.items(), key=lambda x: x[1], reverse=True)
        total_events = sum(hourly_activity.values())
        
        return {
            'peak_hour': sorted_hours[0][0] if sorted_hours else 0,
            'peak_hour_activity': sorted_hours[0][1] if sorted_hours else 0,
            'top_5_hours': [
                {
                    'hour': hour,
                    'activity_count': count,
                    'percentage': round(count/total_events*100, 2)
                }
                for hour, count in sorted_hours[:5]
            ],
            'hourly_distribution': dict(hourly_activity)
        }
    
    def _analyze_lifecycle_stages(self, users: List[Dict]) -> Dict:
        """Classify users by lifecycle stage"""
        
        now = datetime.now(timezone.utc)
        stages = {
            'new': 0,           # < 7 days
            'active': 0,        # 7-30 days, active
            'established': 0,   # > 30 days, active
            'at_risk': 0,       # Not seen in 7-14 days
            'churned': 0        # Not seen in > 14 days
        }
        
        for user in users:
            first_seen = user.get('firstSeen')
            last_seen = user.get('lastSeen')
            
            if isinstance(first_seen, str):
                first_seen = datetime.fromisoformat(first_seen.replace('Z', '+00:00'))
            if isinstance(last_seen, str):
                last_seen = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
            
            days_since_join = (now - first_seen).days if first_seen else 0
            days_since_last = (now - last_seen).days if last_seen else 999
            
            if days_since_last > 14:
                stages['churned'] += 1
            elif days_since_last > 7:
                stages['at_risk'] += 1
            elif days_since_join < 7:
                stages['new'] += 1
            elif days_since_join < 30:
                stages['active'] += 1
            else:
                stages['established'] += 1
        
        total = len(users)
        return {
            stage: {
                'count': count,
                'percentage': round(count/total*100, 2) if total > 0 else 0
            }
            for stage, count in stages.items()
        }
    
    def _calculate_engagement_velocity(self, users: List[Dict], user_events: Dict) -> Dict:
        """Calculate how quickly users progress through content"""
        
        velocities = []
        
        for user in users:
            user_id = user.get('userId')
            total_sessions = user.get('totalSessions', 0)
            total_events = user.get('totalEvents', 0)
            
            first_seen = user.get('firstSeen')
            if isinstance(first_seen, str):
                first_seen = datetime.fromisoformat(first_seen.replace('Z', '+00:00'))
            
            days_active = (datetime.now(timezone.utc) - first_seen).days + 1 if first_seen else 1
            
            # Events per day
            velocity = total_events / days_active if days_active > 0 else 0
            velocities.append(velocity)
        
        if not velocities:
            return {}
        
        return {
            'avg_events_per_day': round(np.mean(velocities), 2),
            'median_events_per_day': round(np.median(velocities), 2),
            'high_velocity_users': len([v for v in velocities if v > np.percentile(velocities, 75)]),
            'low_velocity_users': len([v for v in velocities if v < np.percentile(velocities, 25)])
        }
    
    def _generate_behavior_findings(self, session_patterns, peak_hours, lifecycle) -> List[str]:
        """Generate key behavior findings"""
        
        findings = []
        
        # Session pattern insights
        if session_patterns and session_patterns.get('distribution'):
            dist = session_patterns['distribution']
            dominant_type = max(dist.items(), key=lambda x: x[1]['count'])[0]
            findings.append(
                f"Dominant session type: {dominant_type} "
                f"({dist[dominant_type]['percentage']:.1f}% of sessions)"
            )
        
        # Peak hours insight
        if peak_hours and peak_hours.get('peak_hour') is not None:
            peak_hour = peak_hours['peak_hour']
            findings.append(
                f"Peak activity at {peak_hour:02d}:00 with "
                f"{peak_hours['peak_hour_activity']} events"
            )
        
        # Lifecycle insight
        if lifecycle:
            at_risk_pct = lifecycle.get('at_risk', {}).get('percentage', 0)
            if at_risk_pct > 20:
                findings.append(
                    f"Warning: {at_risk_pct:.1f}% of users are at risk of churning"
                )
        
        return findings
    
    def _analyze_revenue_opportunities(self, economy_events: List[Dict], users: List[Dict]) -> Dict:
        """Identify revenue optimization opportunities"""
        
        if not economy_events:
            return {}
        
        # Calculate conversion rate
        purchases = [e for e in economy_events if e.get('realMoneyValue', 0) > 0]
        payers = set([e.get('globalParams', {}).get('userId') for e in purchases])
        
        conversion_rate = len(payers) / len(users) if users else 0
        
        # Analyze pricing effectiveness
        price_points = defaultdict(lambda: {'count': 0, 'revenue': 0})
        for purchase in purchases:
            price = purchase.get('realMoneyValue', 0)
            price_bucket = self._get_price_bucket(price)
            price_points[price_bucket]['count'] += 1
            price_points[price_bucket]['revenue'] += price
        
        # Identify whale potential (users with high engagement but no purchases)
        whale_candidates = self._identify_whale_candidates(users, economy_events)
        
        # Average transaction value trend
        avg_transaction = np.mean([p.get('realMoneyValue', 0) for p in purchases]) if purchases else 0
        
        return {
            'conversion_rate': round(conversion_rate * 100, 2),
            'total_payers': len(payers),
            'avg_transaction_value': round(avg_transaction, 2),
            'price_point_performance': dict(price_points),
            'whale_candidates': whale_candidates,
            'recommendations': self._generate_revenue_recommendations(
                conversion_rate, price_points, whale_candidates
            )
        }
    
    def _get_price_bucket(self, price: float) -> str:
        """Categorize price into buckets"""
        if price < 1:
            return 'micro'
        elif price < 5:
            return 'small'
        elif price < 20:
            return 'medium'
        elif price < 50:
            return 'large'
        else:
            return 'whale'
    
    def _identify_whale_candidates(self, users: List[Dict], economy_events: List[Dict]) -> List[Dict]:
        """Find users with high potential for whale conversion"""
        
        payers = set([e.get('globalParams', {}).get('userId') for e in economy_events])
        
        candidates = []
        for user in users:
            user_id = user.get('userId')
            if user_id not in payers:
                total_sessions = user.get('totalSessions', 0)
                total_events = user.get('totalEvents', 0)
                
                # High engagement but no purchases
                if total_sessions > 20 and total_events > 500:
                    candidates.append({
                        'user_id': user_id,
                        'sessions': total_sessions,
                        'events': total_events,
                        'engagement_score': total_sessions * 0.3 + total_events * 0.001
                    })
        
        # Sort by engagement score
        candidates.sort(key=lambda x: x['engagement_score'], reverse=True)
        return candidates[:10]
    
    def _generate_revenue_recommendations(self, conversion_rate, price_points, whale_candidates) -> List[str]:
        """Generate revenue optimization recommendations"""
        
        recommendations = []
        
        if conversion_rate < 0.05:
            recommendations.append(
                f"Low conversion rate ({conversion_rate*100:.1f}%). "
                "Consider: 1) Better onboarding, 2) Early value demonstration, 3) First-purchase incentive"
            )
        
        if whale_candidates and len(whale_candidates) > 5:
            recommendations.append(
                f"Found {len(whale_candidates)} high-engagement non-payers. "
                "Target with: 1) Exclusive offers, 2) Premium features trial, 3) VIP status benefits"
            )
        
        # Price point analysis
        if price_points:
            best_bucket = max(price_points.items(), key=lambda x: x[1]['revenue'])[0]
            recommendations.append(
                f"Most revenue from '{best_bucket}' price point. "
                "Consider expanding offerings in this range"
            )
        
        return recommendations
    
    def _analyze_level_balance(self, level_events: List[Dict]) -> Dict:
        """Analyze level difficulty and balance"""
        
        if not level_events:
            return {}
        
        level_stats = defaultdict(lambda: {
            'attempts': 0,
            'completions': 0,
            'failures': 0,
            'playtime': []
        })
        
        for event in level_events:
            level_num = event.get('levelNumber', 0)
            if level_num > 0:
                level_stats[level_num]['attempts'] += 1
                if event.get('completed'):
                    level_stats[level_num]['completions'] += 1
                else:
                    level_stats[level_num]['failures'] += 1
                
                playtime = event.get('levelDuration', 0)
                if playtime > 0:
                    level_stats[level_num]['playtime'].append(playtime / 1000)
        
        # Calculate difficulty scores
        balance_analysis = {}
        for level, stats in level_stats.items():
            completion_rate = stats['completions'] / stats['attempts'] if stats['attempts'] > 0 else 0
            avg_playtime = np.mean(stats['playtime']) if stats['playtime'] else 0
            
            # Difficulty score: lower completion rate = higher difficulty
            difficulty_score = 100 * (1 - completion_rate)
            
            balance_analysis[level] = {
                'completion_rate': round(completion_rate, 3),
                'difficulty_score': round(difficulty_score, 2),
                'avg_playtime_seconds': round(avg_playtime, 2),
                'attempts': stats['attempts']
            }
        
        # Identify problematic levels
        problematic = self._identify_problematic_levels(balance_analysis)
        
        return {
            'level_analysis': balance_analysis,
            'problematic_levels': problematic,
            'recommendations': self._generate_level_recommendations(problematic)
        }
    
    def _identify_problematic_levels(self, balance_analysis: Dict) -> List[Dict]:
        """Identify levels that need rebalancing"""
        
        problematic = []
        
        for level, stats in balance_analysis.items():
            issues = []
            
            if stats['completion_rate'] < 0.3:
                issues.append('very_hard')
            elif stats['completion_rate'] < 0.5:
                issues.append('hard')
            
            if stats['completion_rate'] > 0.95:
                issues.append('too_easy')
            
            if stats['avg_playtime_seconds'] > 300:
                issues.append('too_long')
            
            if issues:
                problematic.append({
                    'level': level,
                    'issues': issues,
                    'stats': stats
                })
        
        return sorted(problematic, key=lambda x: x['level'])
    
    def _generate_level_recommendations(self, problematic: List[Dict]) -> List[str]:
        """Generate level balancing recommendations"""
        
        recommendations = []
        
        very_hard = [p for p in problematic if 'very_hard' in p['issues']]
        if very_hard:
            levels = ', '.join([str(p['level']) for p in very_hard[:5]])
            recommendations.append(
                f"Levels {levels} are extremely difficult (< 30% completion). "
                "Consider: 1) Reducing difficulty, 2) Adding hints, 3) Better tutorials"
            )
        
        too_easy = [p for p in problematic if 'too_easy' in p['issues']]
        if too_easy:
            levels = ', '.join([str(p['level']) for p in too_easy[:5]])
            recommendations.append(
                f"Levels {levels} may be too easy (> 95% completion). "
                "Consider increasing challenge to maintain engagement"
            )
        
        return recommendations
    
    def _predict_engagement_trends(self, users: List[Dict], events: List[Dict]) -> Dict:
        """Predict future engagement trends"""
        
        # Calculate recent trend (last 7 days vs previous 7 days)
        now = datetime.now(timezone.utc)
        recent_cutoff = now - timedelta(days=7)
        previous_cutoff = now - timedelta(days=14)
        
        recent_events = len([
            e for e in events
            if self._parse_timestamp(e) > recent_cutoff
        ])
        
        previous_events = len([
            e for e in events
            if previous_cutoff < self._parse_timestamp(e) <= recent_cutoff
        ])
        
        trend = (recent_events - previous_events) / previous_events if previous_events > 0 else 0
        
        # Project next 7 days
        projected_events = int(recent_events * (1 + trend))
        
        return {
            'trend_direction': 'growing' if trend > 0.05 else 'declining' if trend < -0.05 else 'stable',
            'trend_percentage': round(trend * 100, 2),
            'recent_7_days_events': recent_events,
            'previous_7_days_events': previous_events,
            'projected_next_7_days': projected_events,
            'confidence': self._calculate_trend_confidence(recent_events, previous_events)
        }
    
    def _parse_timestamp(self, event: Dict) -> datetime:
        """Parse timestamp from event"""
        timestamp = event.get('globalParams', {}).get('timestamp', datetime.now(timezone.utc))
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return timestamp
    
    def _calculate_trend_confidence(self, recent: int, previous: int) -> str:
        """Calculate confidence in trend prediction"""
        if recent < 100 or previous < 100:
            return 'low'
        elif recent < 500 or previous < 500:
            return 'medium'
        else:
            return 'high'
    
    def _detect_anomalies(self, events: List[Dict], users: List[Dict]) -> Dict:
        """Detect unusual patterns and anomalies"""
        
        anomalies = []
        
        # Check for unusual event spikes
        event_type_counts = defaultdict(int)
        for event in events:
            event_type = event.get('eventType', 'unknown')
            event_type_counts[event_type] += 1
        
        # Check for suspicious patterns
        total_events = len(events)
        for event_type, count in event_type_counts.items():
            percentage = count / total_events if total_events > 0 else 0
            
            # Flag if any single event type is > 70% of all events
            if percentage > 0.7:
                anomalies.append({
                    'type': 'event_concentration',
                    'severity': 'medium',
                    'description': f"{event_type} represents {percentage*100:.1f}% of all events",
                    'recommendation': 'Investigate if this is expected behavior or data quality issue'
                })
        
        # Check for user activity anomalies
        if users:
            event_counts = [u.get('totalEvents', 0) for u in users]
            if event_counts:
                mean_events = np.mean(event_counts)
                std_events = np.std(event_counts)
                
                # Find outliers (> 3 std deviations)
                outliers = [u for u in users if u.get('totalEvents', 0) > mean_events + 3 * std_events]
                
                if outliers:
                    anomalies.append({
                        'type': 'high_activity_users',
                        'severity': 'low',
                        'description': f"Found {len(outliers)} users with unusually high activity",
                        'recommendation': 'Verify these are legitimate users, not bots'
                    })
        
        return {
            'anomalies_detected': len(anomalies),
            'anomalies': anomalies,
            'status': 'clean' if not anomalies else 'issues_found'
        }
    
    def _ml_player_segmentation(self, users: List[Dict], events: List[Dict]) -> Dict:
        """ML-based player segmentation using clustering"""
        
        if len(users) < 5:
            return {'status': 'insufficient_data', 'min_required': 5}
        
        # Prepare features for clustering
        features = []
        user_ids = []
        
        user_events_map = defaultdict(list)
        for event in events:
            uid = event.get('globalParams', {}).get('userId')
            if uid:
                user_events_map[uid].append(event)
        
        for user in users:
            uid = user.get('userId')
            user_events = user_events_map.get(uid, [])
            
            # Extract features
            total_sessions = user.get('totalSessions', 0)
            total_events = user.get('totalEvents', 0)
            
            # Calculate spending
            spending = sum([
                e.get('realMoneyValue', 0)
                for e in user_events
                if e.get('realMoneyValue')
            ])
            
            # Days active
            first_seen = user.get('firstSeen')
            if isinstance(first_seen, str):
                first_seen = datetime.fromisoformat(first_seen.replace('Z', '+00:00'))
            days_active = (datetime.now(timezone.utc) - first_seen).days + 1 if first_seen else 1
            
            features.append([
                total_sessions,
                total_events,
                spending,
                total_events / days_active if days_active > 0 else 0  # Activity rate
            ])
            user_ids.append(uid)
        
        # Perform K-means clustering
        n_clusters = min(4, len(users))  # Up to 4 segments
        X = np.array(features)
        X_scaled = self.scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        
        # Analyze clusters
        segments = defaultdict(list)
        for idx, label in enumerate(labels):
            segments[int(label)].append({
                'user_id': user_ids[idx],
                'features': features[idx]
            })
        
        # Name segments based on characteristics
        segment_profiles = self._profile_segments(segments)
        
        return {
            'status': 'success',
            'n_segments': n_clusters,
            'segments': segment_profiles
        }
    
    def _profile_segments(self, segments: Dict) -> Dict:
        """Profile each segment based on average characteristics"""
        
        profiles = {}
        
        segment_names = ['High Value', 'Engaged', 'Casual', 'New/Low Activity']
        
        for idx, (segment_id, users) in enumerate(segments.items()):
            features = np.array([u['features'] for u in users])
            
            avg_sessions = np.mean(features[:, 0])
            avg_events = np.mean(features[:, 1])
            avg_spending = np.mean(features[:, 2])
            avg_activity_rate = np.mean(features[:, 3])
            
            # Determine segment name based on characteristics
            if avg_spending > 10:
                name = 'Whales (High Spenders)'
            elif avg_activity_rate > 50:
                name = 'Super Engaged'
            elif avg_sessions > 15:
                name = 'Engaged Players'
            elif avg_sessions > 5:
                name = 'Casual Players'
            else:
                name = 'New/Inactive'
            
            profiles[segment_id] = {
                'name': name,
                'size': len(users),
                'avg_sessions': round(avg_sessions, 2),
                'avg_events': round(avg_events, 2),
                'avg_spending': round(avg_spending, 2),
                'avg_daily_activity': round(avg_activity_rate, 2)
            }
        
        return profiles
    
    def _identify_retention_drivers(self, users: List[Dict], events: List[Dict]) -> Dict:
        """Identify factors that drive retention"""
        
        # Compare retained vs churned users
        now = datetime.now(timezone.utc)
        churned_threshold = now - timedelta(days=14)
        
        retained = []
        churned = []
        
        for user in users:
            last_seen = user.get('lastSeen')
            if isinstance(last_seen, str):
                last_seen = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
            
            if last_seen > churned_threshold:
                retained.append(user)
            else:
                churned.append(user)
        
        if not retained or not churned:
            return {'status': 'insufficient_data'}
        
        # Compare characteristics
        retained_sessions = np.mean([u.get('totalSessions', 0) for u in retained])
        churned_sessions = np.mean([u.get('totalSessions', 0) for u in churned])
        
        retained_events = np.mean([u.get('totalEvents', 0) for u in retained])
        churned_events = np.mean([u.get('totalEvents', 0) for u in churned])
        
        return {
            'retained_users': len(retained),
            'churned_users': len(churned),
            'session_impact': {
                'retained_avg': round(retained_sessions, 2),
                'churned_avg': round(churned_sessions, 2),
                'difference': round(retained_sessions - churned_sessions, 2)
            },
            'event_impact': {
                'retained_avg': round(retained_events, 2),
                'churned_avg': round(churned_events, 2),
                'difference': round(retained_events - churned_events, 2)
            },
            'key_drivers': self._identify_key_drivers(retained, churned)
        }
    
    def _identify_key_drivers(self, retained: List[Dict], churned: List[Dict]) -> List[str]:
        """Identify key retention drivers"""
        
        drivers = []
        
        retained_sessions = np.mean([u.get('totalSessions', 0) for u in retained])
        churned_sessions = np.mean([u.get('totalSessions', 0) for u in churned])
        
        if retained_sessions > churned_sessions * 1.5:
            drivers.append(
                f"Session frequency strongly correlated with retention "
                f"(retained users have {(retained_sessions/churned_sessions - 1)*100:.0f}% more sessions)"
            )
        
        # Check platforms
        retained_platforms = defaultdict(int)
        churned_platforms = defaultdict(int)
        
        for u in retained:
            retained_platforms[u.get('platform', 'unknown')] += 1
        for u in churned:
            churned_platforms[u.get('platform', 'unknown')] += 1
        
        # Find platform with best retention
        best_platform = None
        best_ratio = 0
        for platform in retained_platforms:
            if platform in churned_platforms:
                ratio = retained_platforms[platform] / churned_platforms[platform]
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_platform = platform
        
        if best_platform and best_ratio > 1.5:
            drivers.append(
                f"Platform '{best_platform}' shows higher retention "
                f"({best_ratio:.1f}x better than others)"
            )
        
        return drivers or ["Need more data to identify specific drivers"]
    
    def _analyze_monetization_patterns(self, economy_events: List[Dict], users: List[Dict]) -> Dict:
        """Deep dive into monetization patterns"""
        
        if not economy_events:
            return {}
        
        purchases = [e for e in economy_events if e.get('realMoneyValue', 0) > 0]
        
        # Time to first purchase
        user_first_purchase = {}
        for purchase in purchases:
            uid = purchase.get('globalParams', {}).get('userId')
            timestamp = purchase.get('globalParams', {}).get('timestamp')
            
            if uid and timestamp:
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                
                if uid not in user_first_purchase or timestamp < user_first_purchase[uid]:
                    user_first_purchase[uid] = timestamp
        
        # Calculate time to first purchase
        time_to_purchase = []
        for user in users:
            uid = user.get('userId')
            if uid in user_first_purchase:
                first_seen = user.get('firstSeen')
                if isinstance(first_seen, str):
                    first_seen = datetime.fromisoformat(first_seen.replace('Z', '+00:00'))
                
                if first_seen:
                    days_to_purchase = (user_first_purchase[uid] - first_seen).days
                    time_to_purchase.append(days_to_purchase)
        
        avg_time_to_purchase = np.mean(time_to_purchase) if time_to_purchase else 0
        
        # Purchase frequency
        user_purchase_counts = defaultdict(int)
        for purchase in purchases:
            uid = purchase.get('globalParams', {}).get('userId')
            if uid:
                user_purchase_counts[uid] += 1
        
        repeat_purchasers = len([c for c in user_purchase_counts.values() if c > 1])
        
        return {
            'avg_days_to_first_purchase': round(avg_time_to_purchase, 2),
            'repeat_purchaser_rate': round(repeat_purchasers / len(user_purchase_counts), 3) if user_purchase_counts else 0,
            'total_purchasing_users': len(user_purchase_counts),
            'avg_purchases_per_payer': round(np.mean(list(user_purchase_counts.values())), 2) if user_purchase_counts else 0
        }
    
    def _generate_content_recommendations(self, level_events: List[Dict], users: List[Dict]) -> Dict:
        """Generate content strategy recommendations"""
        
        if not level_events:
            return {}
        
        # Analyze level completion rates
        max_level = max([e.get('levelNumber', 0) for e in level_events]) if level_events else 0
        
        # Calculate content exhaustion risk
        users_at_max = len([
            u for u in users
            if any(e.get('levelNumber') == max_level for e in level_events 
                   if e.get('globalParams', {}).get('userId') == u.get('userId'))
        ])
        
        exhaustion_risk = users_at_max / len(users) if users else 0
        
        recommendations = []
        
        if exhaustion_risk > 0.1:
            recommendations.append({
                'priority': 'high',
                'type': 'content_expansion',
                'message': f"{users_at_max} users ({exhaustion_risk*100:.1f}%) have reached max level. Add new content urgently.",
                'suggested_levels': 10
            })
        
        if max_level < 50:
            recommendations.append({
                'priority': 'medium',
                'type': 'content_depth',
                'message': f"Only {max_level} levels available. Consider adding more content for long-term engagement.",
                'suggested_levels': 50 - max_level
            })
        
        return {
            'max_level': max_level,
            'users_at_max': users_at_max,
            'exhaustion_risk': round(exhaustion_risk, 3),
            'recommendations': recommendations
        }
    
    def _assess_business_risks(self, churn_predictions: List[Dict], users: List[Dict], economy_events: List[Dict]) -> Dict:
        """Assess overall business health risks"""
        
        risks = []
        
        # Churn risk
        if churn_predictions:
            high_risk = len([p for p in churn_predictions if p.get('churn_risk') in ['high', 'critical']])
            high_risk_pct = high_risk / len(users) if users else 0
            
            if high_risk_pct > 0.3:
                risks.append({
                    'category': 'churn',
                    'severity': 'critical',
                    'impact': f"{high_risk_pct*100:.1f}% of users at high churn risk",
                    'recommendation': 'Launch retention campaign immediately'
                })
            elif high_risk_pct > 0.15:
                risks.append({
                    'category': 'churn',
                    'severity': 'high',
                    'impact': f"{high_risk_pct*100:.1f}% of users at risk",
                    'recommendation': 'Implement re-engagement strategies'
                })
        
        # Revenue concentration risk
        purchases = [e for e in economy_events if e.get('realMoneyValue', 0) > 0]
        if purchases:
            user_spending = defaultdict(float)
            for p in purchases:
                uid = p.get('globalParams', {}).get('userId')
                if uid:
                    user_spending[uid] += p.get('realMoneyValue', 0)
            
            if user_spending:
                total_revenue = sum(user_spending.values())
                top_spender = max(user_spending.values())
                concentration = top_spender / total_revenue if total_revenue > 0 else 0
                
                if concentration > 0.5:
                    risks.append({
                        'category': 'revenue_concentration',
                        'severity': 'high',
                        'impact': f"Single user represents {concentration*100:.1f}% of revenue",
                        'recommendation': 'Diversify revenue sources'
                    })
        
        return {
            'total_risks': len(risks),
            'risks': risks,
            'overall_health': 'critical' if any(r['severity'] == 'critical' for r in risks) else 'warning' if risks else 'healthy'
        }
    
    def _calculate_opportunity_scores(self, users: List[Dict], events: List[Dict], economy_events: List[Dict]) -> Dict:
        """Calculate actionable opportunity scores"""
        
        opportunities = {
            'monetization': 0,
            'engagement': 0,
            'retention': 0,
            'growth': 0
        }
        
        # Monetization opportunity (non-paying engaged users)
        payers = set([e.get('globalParams', {}).get('userId') for e in economy_events])
        engaged_non_payers = len([
            u for u in users
            if u.get('totalSessions', 0) > 10 and u.get('userId') not in payers
        ])
        opportunities['monetization'] = min(100, engaged_non_payers * 5)
        
        # Engagement opportunity (low activity users)
        low_activity = len([u for u in users if u.get('totalSessions', 0) < 5])
        opportunities['engagement'] = min(100, low_activity * 3)
        
        # Retention opportunity (at-risk users)
        now = datetime.now(timezone.utc)
        at_risk = len([
            u for u in users
            if (now - self._parse_user_date(u.get('lastSeen'))).days > 7
        ])
        opportunities['retention'] = min(100, at_risk * 4)
        
        # Growth opportunity (viral coefficient, social features)
        avg_sessions = np.mean([u.get('totalSessions', 0) for u in users]) if users else 0
        if avg_sessions > 20:
            opportunities['growth'] = 75  # High engagement suggests viral potential
        elif avg_sessions > 10:
            opportunities['growth'] = 50
        else:
            opportunities['growth'] = 25
        
        return opportunities
    
    def _parse_user_date(self, date_val):
        """Parse user date safely"""
        if isinstance(date_val, datetime):
            return date_val
        if isinstance(date_val, str):
            return datetime.fromisoformat(date_val.replace('Z', '+00:00'))
        return datetime.now(timezone.utc)
    
    def _generate_executive_summary(self, insights: Dict) -> Dict:
        """Generate high-level executive summary"""
        
        summary = {
            'health_status': 'healthy',
            'top_priorities': [],
            'key_metrics': {},
            'quick_wins': []
        }
        
        # Determine overall health
        risks = insights.get('risk_assessment', {})
        if risks.get('overall_health') == 'critical':
            summary['health_status'] = 'critical'
        elif risks.get('overall_health') == 'warning':
            summary['health_status'] = 'warning'
        
        # Extract top priorities from risks
        if risks.get('risks'):
            for risk in risks['risks'][:3]:
                summary['top_priorities'].append({
                    'priority': risk['category'],
                    'action': risk['recommendation']
                })
        
        # Key opportunities
        opportunities = insights.get('opportunity_score', {})
        if opportunities:
            best_opportunity = max(opportunities.items(), key=lambda x: x[1])
            summary['key_metrics']['best_opportunity'] = {
                'area': best_opportunity[0],
                'score': best_opportunity[1]
            }
        
        # Quick wins
        revenue_opts = insights.get('revenue_optimization', {})
        if revenue_opts.get('whale_candidates'):
            summary['quick_wins'].append(
                f"Target {len(revenue_opts['whale_candidates'])} high-potential users for conversion"
            )
        
        return summary

