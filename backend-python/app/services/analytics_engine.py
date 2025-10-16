"""
Real-time Analytics Engine
Aggregates and processes game analytics data
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta, timezone
from collections import defaultdict


class AnalyticsEngine:
    """
    Central analytics processing engine
    
    Provides:
    - Real-time user metrics (DAU, MAU, concurrent players)
    - Session analytics  
    - Level distribution
    - Revenue metrics
    - Engagement trends
    - Retention analysis
    """
    
    def get_overview_metrics(
        self,
        users: List[Dict],
        all_events: List[Dict],
        game_events: List[Dict],
        level_events: List[Dict],
        economy_events: List[Dict]
    ) -> Dict:
        """Get comprehensive overview of all metrics"""
        
        now = datetime.now(timezone.utc)
        
        # Calculate time-based metrics
        dau = self._calculate_dau(users, now)
        wau = self._calculate_wau(users, now)
        mau = self._calculate_mau(users, now)
        
        # User metrics
        total_users = len(users)
        new_users_today = self._count_new_users(users, now, days=1)
        new_users_week = self._count_new_users(users, now, days=7)
        
        # Engagement metrics
        avg_sessions_per_user = np.mean([u.get('totalSessions', 0) for u in users]) if users else 0
        avg_events_per_user = np.mean([u.get('totalEvents', 0) for u in users]) if users else 0
        
        # Session metrics from game events
        session_metrics = self._calculate_session_metrics(game_events)
        
        # Level metrics
        level_metrics = self._calculate_level_metrics(level_events)
        
        # Revenue metrics
        revenue_metrics = self._calculate_revenue_metrics(economy_events)
        
        # Platform distribution
        platform_dist = self._calculate_platform_distribution(users)
        
        # Retention rates
        retention = self._calculate_retention_rates(users, all_events, now)
        
        return {
            'timestamp': now.isoformat(),
            'user_metrics': {
                'total_users': total_users,
                'dau': dau,
                'wau': wau,
                'mau': mau,
                'new_users_today': new_users_today,
                'new_users_this_week': new_users_week,
                'dau_mau_ratio': round(dau / mau, 3) if mau > 0 else 0,
                'avg_sessions_per_user': round(avg_sessions_per_user, 2),
                'avg_events_per_user': round(avg_events_per_user, 2)
            },
            'session_metrics': session_metrics,
            'level_metrics': level_metrics,
            'revenue_metrics': revenue_metrics,
            'platform_distribution': platform_dist,
            'retention_rates': retention,
            'total_events_tracked': len(all_events)
        }
    
    def _calculate_dau(self, users: List[Dict], now: datetime) -> int:
        """Daily Active Users"""
        yesterday = now - timedelta(days=1)
        return len([
            u for u in users
            if self._parse_date(u.get('lastSeen')) > yesterday
        ])
    
    def _calculate_wau(self, users: List[Dict], now: datetime) -> int:
        """Weekly Active Users"""
        week_ago = now - timedelta(days=7)
        return len([
            u for u in users
            if self._parse_date(u.get('lastSeen')) > week_ago
        ])
    
    def _calculate_mau(self, users: List[Dict], now: datetime) -> int:
        """Monthly Active Users"""
        month_ago = now - timedelta(days=30)
        return len([
            u for u in users
            if self._parse_date(u.get('lastSeen')) > month_ago
        ])
    
    def _count_new_users(self, users: List[Dict], now: datetime, days: int) -> int:
        """Count users who joined in last N days"""
        cutoff = now - timedelta(days=days)
        return len([
            u for u in users
            if self._parse_date(u.get('firstSeen')) > cutoff
        ])
    
    def _parse_date(self, date_str) -> datetime:
        """Parse date string to datetime"""
        if isinstance(date_str, datetime):
            # Ensure datetime is timezone-aware
            if date_str.tzinfo is None:
                return date_str.replace(tzinfo=timezone.utc)
            return date_str
        if isinstance(date_str, str):
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return datetime.min.replace(tzinfo=timezone.utc)
    
    def _calculate_session_metrics(self, game_events: List[Dict]) -> Dict:
        """Calculate session-related metrics"""
        if not game_events:
            return self._empty_session_metrics()
        
        # Extract session data
        session_durations = []
        active_sessions = set()
        
        for event in game_events:
            global_params = event.get('globalParams', {})
            session_id = global_params.get('sessionId')
            duration = global_params.get('sessionDuration', 0)
            
            if session_id:
                active_sessions.add(session_id)
            if duration > 0:
                session_durations.append(duration / 1000 / 60)  # Convert to minutes
        
        return {
            'total_sessions': len(active_sessions),
            'avg_session_duration_minutes': round(np.mean(session_durations), 2) if session_durations else 0,
            'median_session_duration_minutes': round(np.median(session_durations), 2) if session_durations else 0,
            'longest_session_minutes': round(max(session_durations), 2) if session_durations else 0,
            'total_playtime_hours': round(sum(session_durations) / 60, 2) if session_durations else 0
        }
    
    def _calculate_level_metrics(self, level_events: List[Dict]) -> Dict:
        """Calculate level-related metrics"""
        if not level_events:
            return self._empty_level_metrics()
        
        total_attempts = len(level_events)
        completed = len([e for e in level_events if e.get('completed', False)])
        
        # Level distribution
        level_counts = defaultdict(int)
        for event in level_events:
            level_num = event.get('levelNumber', 0)
            if level_num > 0:
                level_counts[level_num] += 1
        
        max_level_reached = max(level_counts.keys()) if level_counts else 0
        
        # Most played levels
        most_played = sorted(level_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_level_attempts': total_attempts,
            'total_level_completions': completed,
            'overall_completion_rate': round(completed / total_attempts, 3) if total_attempts > 0 else 0,
            'max_level_reached': max_level_reached,
            'unique_levels_played': len(level_counts),
            'most_played_levels': [
                {'level': lvl, 'attempts': count} 
                for lvl, count in most_played
            ]
        }
    
    def _calculate_revenue_metrics(self, economy_events: List[Dict]) -> Dict:
        """Calculate revenue and monetization metrics"""
        if not economy_events:
            return self._empty_revenue_metrics()
        
        # Filter purchase events
        purchases = [
            e for e in economy_events
            if e.get('realMoneyValue', 0) > 0
        ]
        
        total_revenue = sum([e.get('realMoneyValue', 0) for e in purchases])
        total_transactions = len(purchases)
        
        # Unique payers
        payers = set([
            e.get('globalParams', {}).get('userId')
            for e in purchases
            if e.get('globalParams', {}).get('userId')
        ])
        paying_users = len(payers)
        
        # ARPU and ARPPU calculation would need total users
        avg_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0
        
        # Currency distribution
        currency_types = defaultdict(lambda: {'count': 0, 'amount': 0})
        for event in economy_events:
            currency = event.get('currencyType', 'unknown')
            amount = event.get('amount', 0)
            currency_types[currency]['count'] += 1
            currency_types[currency]['amount'] += amount
        
        return {
            'total_revenue': round(total_revenue, 2),
            'total_transactions': total_transactions,
            'paying_users': paying_users,
            'avg_transaction_value': round(avg_transaction_value, 2),
            'revenue_per_paying_user': round(total_revenue / paying_users, 2) if paying_users > 0 else 0,
            'virtual_currency_stats': dict(currency_types)
        }
    
    def _calculate_platform_distribution(self, users: List[Dict]) -> Dict:
        """Calculate distribution across platforms"""
        platforms = defaultdict(int)
        for user in users:
            platform = user.get('platform', 'unknown')
            platforms[platform] += 1
        
        total = len(users)
        return {
            platform: {
                'count': count,
                'percentage': round(count / total * 100, 2) if total > 0 else 0
            }
            for platform, count in platforms.items()
        }
    
    def _calculate_retention_rates(
        self, 
        users: List[Dict], 
        events: List[Dict],
        now: datetime
    ) -> Dict:
        """Calculate retention rates"""
        # This is a simplified calculation
        # For accurate retention, we'd need cohort analysis
        
        # Day 1 retention (users who came back next day)
        retention_data = {
            'day_1': 0,
            'day_7': 0,
            'day_30': 0
        }
        
        # Group events by user
        user_activity = defaultdict(list)
        for event in events:
            user_id = event.get('globalParams', {}).get('userId')
            timestamp = event.get('globalParams', {}).get('timestamp')
            if user_id and timestamp:
                user_activity[user_id].append(self._parse_date(timestamp))
        
        # Calculate retention for users who joined 30+ days ago
        eligible_users = [
            u for u in users
            if (now - self._parse_date(u.get('firstSeen'))).days >= 30
        ]
        
        if eligible_users:
            for user in eligible_users:
                user_id = user.get('userId')
                first_seen = self._parse_date(user.get('firstSeen'))
                
                if user_id in user_activity:
                    activity_dates = user_activity[user_id]
                    
                    # Check if user was active on day 1, 7, 30
                    for day in [1, 7, 30]:
                        target_date = first_seen + timedelta(days=day)
                        if any(abs((d - target_date).days) <= 1 for d in activity_dates):
                            retention_data[f'day_{day}'] += 1
            
            # Calculate percentages
            total = len(eligible_users)
            return {
                'day_1_retention': round(retention_data['day_1'] / total * 100, 2) if total > 0 else 0,
                'day_7_retention': round(retention_data['day_7'] / total * 100, 2) if total > 0 else 0,
                'day_30_retention': round(retention_data['day_30'] / total * 100, 2) if total > 0 else 0,
                'cohort_size': total
            }
        
        return {
            'day_1_retention': 0,
            'day_7_retention': 0,
            'day_30_retention': 0,
            'cohort_size': 0
        }
    
    def get_user_segments(self, users: List[Dict], events: List[Dict]) -> Dict:
        """Segment users by behavior"""
        now = datetime.now(timezone.utc)
        
        segments = {
            'whales': [],  # High spenders
            'engaged': [],  # High activity
            'casual': [],  # Low activity
            'at_risk': [],  # Declining activity
            'new': [],  # Recently joined
            'dormant': []  # Inactive
        }
        
        # Group events by user for analysis
        user_events = defaultdict(list)
        for event in events:
            user_id = event.get('globalParams', {}).get('userId')
            if user_id:
                user_events[user_id].append(event)
        
        for user in users:
            user_id = user.get('userId')
            last_seen = self._parse_date(user.get('lastSeen'))
            first_seen = self._parse_date(user.get('firstSeen'))
            days_since_last = (now - last_seen).days
            days_since_first = (now - first_seen).days
            
            total_sessions = user.get('totalSessions', 0)
            user_event_list = user_events.get(user_id, [])
            
            # Calculate spending
            total_spent = sum([
                e.get('realMoneyValue', 0)
                for e in user_event_list
                if e.get('realMoneyValue')
            ])
            
            # Segment logic
            if total_spent > 50:
                segments['whales'].append(user_id)
            
            if days_since_first <= 7:
                segments['new'].append(user_id)
            
            if days_since_last > 14:
                segments['dormant'].append(user_id)
            elif days_since_last > 7:
                segments['at_risk'].append(user_id)
            elif total_sessions > 20:
                segments['engaged'].append(user_id)
            elif total_sessions > 0:
                segments['casual'].append(user_id)
        
        return {
            segment: {
                'count': len(user_ids),
                'percentage': round(len(user_ids) / len(users) * 100, 2) if users else 0
            }
            for segment, user_ids in segments.items()
        }
    
    def _empty_session_metrics(self) -> Dict:
        return {
            'total_sessions': 0,
            'avg_session_duration_minutes': 0,
            'median_session_duration_minutes': 0,
            'longest_session_minutes': 0,
            'total_playtime_hours': 0
        }
    
    def _empty_level_metrics(self) -> Dict:
        return {
            'total_level_attempts': 0,
            'total_level_completions': 0,
            'overall_completion_rate': 0,
            'max_level_reached': 0,
            'unique_levels_played': 0,
            'most_played_levels': []
        }
    
    def _empty_revenue_metrics(self) -> Dict:
        return {
            'total_revenue': 0,
            'total_transactions': 0,
            'paying_users': 0,
            'avg_transaction_value': 0,
            'revenue_per_paying_user': 0,
            'virtual_currency_stats': {}
        }
