"""
AI-Powered Game Recommendations Engine
Provides actionable insights for game improvement
"""
from typing import Dict, List
import numpy as np


class GameRecommendations:
    """
    AI-powered recommendation system for game developers
    
    Analyzes:
    - Level difficulty balance
    - User retention strategies
    - Monetization optimization
    - Content gaps
    - Engagement improvements
    """
    
    def generate_comprehensive_recommendations(
        self,
        overview_metrics: Dict,
        level_analysis: Dict,
        churn_analysis: List[Dict],
        user_segments: Dict
    ) -> Dict:
        """Generate comprehensive game improvement recommendations"""
        
        recommendations = {
            'critical': [],  # Urgent issues
            'high_priority': [],  # Important improvements
            'medium_priority': [],  # Good to have
            'low_priority': [],  # Minor optimizations
            'positive_insights': []  # What's working well
        }
        
        # Analyze different aspects
        recommendations = self._analyze_retention(recommendations, overview_metrics, churn_analysis)
        recommendations = self._analyze_level_difficulty(recommendations, level_analysis)
        recommendations = self._analyze_monetization(recommendations, overview_metrics, user_segments)
        recommendations = self._analyze_engagement(recommendations, overview_metrics)
        recommendations = self._analyze_user_progression(recommendations, level_analysis)
        recommendations = self._identify_positive_patterns(recommendations, overview_metrics, level_analysis)
        
        # Add priority scores
        for priority in recommendations:
            if isinstance(recommendations[priority], list):
                for item in recommendations[priority]:
                    if isinstance(item, dict) and 'priority_score' not in item:
                        item['priority_score'] = self._calculate_priority_score(item, priority)
        
        return recommendations
    
    def _analyze_retention(
        self,
        recommendations: Dict,
        metrics: Dict,
        churn_analysis: List[Dict]
    ) -> Dict:
        """Analyze retention and churn"""
        retention = metrics.get('retention_rates', {})
        user_metrics = metrics.get('user_metrics', {})
        
        day_1_retention = retention.get('day_1_retention', 0)
        day_7_retention = retention.get('day_7_retention', 0)
        dau_mau = user_metrics.get('dau_mau_ratio', 0)
        
        # Critical retention issues
        if day_1_retention < 40:
            recommendations['critical'].append({
                'category': 'Retention',
                'issue': f'Very low Day 1 retention ({day_1_retention}%)',
                'impact': 'High user drop-off after first session',
                'recommendations': [
                    'Improve first-time user experience (FTUE)',
                    'Add tutorial skip option for experienced players',
                    'Provide immediate rewards in first session',
                    'Reduce barriers to core gameplay loop',
                    'Send push notification 24 hours after first session'
                ],
                'expected_improvement': '15-25% increase in Day 1 retention'
            })
        elif day_1_retention < 60:
            recommendations['high_priority'].append({
                'category': 'Retention',
                'issue': f'Below average Day 1 retention ({day_1_retention}%)',
                'recommendations': [
                    'Optimize onboarding flow',
                    'Add progression rewards',
                    'Implement better tutorial'
                ]
            })
        
        # Day 7 retention
        if day_7_retention < 20:
            recommendations['high_priority'].append({
                'category': 'Retention',
                'issue': f'Low Day 7 retention ({day_7_retention}%)',
                'impact': 'Players not forming habit',
                'recommendations': [
                    'Implement daily login bonuses',
                    'Add time-limited events',
                    'Create compelling meta-progression system',
                    'Introduce social features',
                    'Send re-engagement notifications'
                ]
            })
        
        # DAU/MAU ratio (stickiness)
        if dau_mau < 0.15:
            recommendations['high_priority'].append({
                'category': 'Engagement',
                'issue': f'Low DAU/MAU ratio ({dau_mau:.2%}) indicates low stickiness',
                'recommendations': [
                    'Add daily quests or challenges',
                    'Implement energy/stamina system to encourage multiple sessions',
                    'Create reasons to return daily',
                    'Add guild or clan features'
                ]
            })
        
        # High churn risk users
        high_churn_count = len([c for c in churn_analysis if c.get('churn_risk') in ['high', 'critical']])
        if high_churn_count > 0:
            recommendations['high_priority'].append({
                'category': 'Churn Prevention',
                'issue': f'{high_churn_count} users at high/critical churn risk',
                'recommendations': [
                    'Send targeted re-engagement campaigns',
                    'Offer personalized incentives',
                    'Identify common patterns in at-risk users',
                    'Create win-back offers'
                ],
                'action_required': 'Review individual users in PAIME dashboard'
            })
        
        return recommendations
    
    def _analyze_level_difficulty(
        self,
        recommendations: Dict,
        level_analysis: Dict
    ) -> Dict:
        """Analyze level difficulty and progression"""
        drop_off_levels = level_analysis.get('drop_off_levels', [])
        bottlenecks = level_analysis.get('bottleneck_levels', [])
        hardest = level_analysis.get('hardest_levels', [])
        
        # Critical drop-off levels
        critical_drop_offs = [l for l in drop_off_levels if l.get('severity') == 'critical']
        if critical_drop_offs:
            for level in critical_drop_offs[:3]:  # Top 3
                recommendations['critical'].append({
                    'category': 'Level Difficulty',
                    'issue': f"Critical drop-off at {level['level_id']} (only {level['completion_rate']:.1%} complete)",
                    'impact': f"{level['players_stuck']} players stuck",
                    'recommendations': [
                        'Reduce difficulty or add checkpoints',
                        'Provide skip option after 5+ fails',
                        'Add hint system',
                        'Rebalance enemy/obstacle placement',
                        'Consider level redesign'
                    ],
                    'metrics': {
                        'completion_rate': level['completion_rate'],
                        'difficulty_score': level['difficulty_score']
                    }
                })
        
        # Bottleneck levels
        if bottlenecks:
            for level in bottlenecks[:2]:  # Top 2
                recommendations['high_priority'].append({
                    'category': 'Level Difficulty',
                    'issue': f"Bottleneck at {level['level_id']} - high traffic, low completion",
                    'recommendations': [
                        f"Add difficulty options (easy/normal/hard)",
                        'Improve level guidance',
                        'Add practice mode',
                        'Balance reward vs difficulty'
                    ],
                    'metrics': level
                })
        
        # Difficulty curve analysis
        if hardest and len(hardest) > 3:
            difficulty_scores = [
                level_analysis.get('difficulty_scores', {}).get(lvl, 0)
                for lvl in hardest
            ]
            avg_hardest = np.mean(difficulty_scores) if difficulty_scores else 0
            
            if avg_hardest > 80:
                recommendations['medium_priority'].append({
                    'category': 'Level Design',
                    'issue': 'Several extremely difficult levels may frustrate players',
                    'recommendations': [
                        'Review difficulty curve across game',
                        'Add gradual difficulty ramp',
                        'Place extremely hard levels as optional challenges',
                        'Consider adaptive difficulty'
                    ]
                })
        
        return recommendations
    
    def _analyze_monetization(
        self,
        recommendations: Dict,
        metrics: Dict,
        user_segments: Dict
    ) -> Dict:
        """Analyze monetization opportunities"""
        revenue = metrics.get('revenue_metrics', {})
        user_count = metrics.get('user_metrics', {}).get('total_users', 0)
        
        total_revenue = revenue.get('total_revenue', 0)
        paying_users = revenue.get('paying_users', 0)
        conversion_rate = (paying_users / user_count * 100) if user_count > 0 else 0
        
        # Low conversion rate
        if conversion_rate < 2 and user_count > 100:
            recommendations['high_priority'].append({
                'category': 'Monetization',
                'issue': f'Low conversion rate ({conversion_rate:.2f}%)',
                'recommendations': [
                    'Improve first-time buyer offers',
                    'Add limited-time sales',
                    'Create better value propositions',
                    'Implement starter packs',
                    'Show benefits of premium features clearly',
                    'A/B test pricing'
                ],
                'potential_impact': f'Industry average is 2-5%, could double revenue'
            })
        
        # Analyze segments
        segments = user_segments
        engaged_pct = segments.get('engaged', {}).get('percentage', 0)
        whales_pct = segments.get('whales', {}).get('percentage', 0)
        
        if engaged_pct > 10 and conversion_rate < 3:
            recommendations['medium_priority'].append({
                'category': 'Monetization',
                'issue': 'High engagement but low monetization',
                'recommendations': [
                    'Add more cosmetic items',
                    'Implement season pass',
                    'Create VIP membership',
                    'Add quality-of-life purchases',
                    'Introduce battle pass system'
                ]
            })
        
        # Revenue per paying user
        arpu = revenue.get('revenue_per_paying_user', 0)
        if arpu < 5 and paying_users > 10:
            recommendations['medium_priority'].append({
                'category': 'Monetization',
                'issue': f'Low ARPPU (${arpu:.2f})',
                'recommendations': [
                    'Add premium content for whales',
                    'Create exclusive items',
                    'Implement bundle deals',
                    'Add subscription options'
                ]
            })
        
        return recommendations
    
    def _analyze_engagement(
        self,
        recommendations: Dict,
        metrics: Dict
    ) -> Dict:
        """Analyze engagement patterns"""
        session_metrics = metrics.get('session_metrics', {})
        user_metrics = metrics.get('user_metrics', {})
        
        avg_session_duration = session_metrics.get('avg_session_duration_minutes', 0)
        avg_sessions_per_user = user_metrics.get('avg_sessions_per_user', 0)
        
        # Short sessions
        if avg_session_duration < 5:
            recommendations['medium_priority'].append({
                'category': 'Engagement',
                'issue': f'Short average session duration ({avg_session_duration:.1f} minutes)',
                'recommendations': [
                    'Add more engaging core loop',
                    'Implement progression hooks',
                    'Create "one more turn" mechanics',
                    'Add meta-game features',
                    'Improve reward pacing'
                ]
            })
        
        # Low session frequency
        if avg_sessions_per_user < 5:
            recommendations['medium_priority'].append({
                'category': 'Engagement',
                'issue': 'Low average sessions per user',
                'recommendations': [
                    'Add reasons to return',
                    'Implement notifications strategically',
                    'Create daily rewards',
                    'Add limited-time content'
                ]
            })
        
        return recommendations
    
    def _analyze_user_progression(
        self,
        recommendations: Dict,
        level_analysis: Dict
    ) -> Dict:
        """Analyze user progression through content"""
        funnel = level_analysis.get('level_progression_funnel', {})
        funnel_data = funnel.get('funnel', [])
        
        if funnel_data and len(funnel_data) > 5:
            # Find biggest drop-off
            biggest_drop = max(
                funnel_data,
                key=lambda x: x.get('drop_off_rate', 0),
                default=None
            )
            
            if biggest_drop and biggest_drop.get('drop_off_rate', 0) > 0.3:
                recommendations['high_priority'].append({
                    'category': 'Content Progression',
                    'issue': f"Major drop-off at level {biggest_drop['level_number']} ({biggest_drop['drop_off_rate']:.1%} don't continue)",
                    'recommendations': [
                        'Investigate level design',
                        'Check if difficulty spike',
                        'Add incentive to continue',
                        'Review monetization gates',
                        'Consider level reordering'
                    ]
                })
        
        # Content exhaustion
        level_stats = level_analysis.get('level_stats', {})
        if level_stats:
            max_level = max([
                stats.get('level_number', 0) 
                for stats in level_stats.values()
            ], default=0)
            
            if max_level < 20:
                recommendations['high_priority'].append({
                    'category': 'Content',
                    'issue': f'Limited content ({max_level} levels)',
                    'recommendations': [
                        'Add more levels to increase lifetime value',
                        'Create endless mode',
                        'Add procedural content',
                        'Implement level editor',
                        'Add challenge modes'
                    ]
                })
        
        return recommendations
    
    def _identify_positive_patterns(
        self,
        recommendations: Dict,
        metrics: Dict,
        level_analysis: Dict
    ) -> Dict:
        """Identify what's working well"""
        retention = metrics.get('retention_rates', {})
        revenue = metrics.get('revenue_metrics', {})
        user_metrics = metrics.get('user_metrics', {})
        
        day_1_retention = retention.get('day_1_retention', 0)
        day_7_retention = retention.get('day_7_retention', 0)
        dau_mau = user_metrics.get('dau_mau_ratio', 0)
        conversion_rate = (revenue.get('paying_users', 0) / user_metrics.get('total_users', 1)) * 100
        
        # Good retention
        if day_1_retention > 60:
            recommendations['positive_insights'].append({
                'achievement': f'Excellent Day 1 retention ({day_1_retention}%)',
                'insight': 'Onboarding and first-time experience are working well',
                'recommendation': 'Document what makes FTUE successful for future games'
            })
        
        if day_7_retention > 30:
            recommendations['positive_insights'].append({
                'achievement': f'Strong Day 7 retention ({day_7_retention}%)',
                'insight': 'Players are forming habits and enjoying the game',
                'recommendation': 'Maintain core loop, iterate on meta features'
            })
        
        # Good monetization
        if conversion_rate > 3:
            recommendations['positive_insights'].append({
                'achievement': f'Good conversion rate ({conversion_rate:.2f}%)',
                'insight': 'Monetization is well-balanced',
                'recommendation': 'Consider scaling marketing efforts'
            })
        
        # Easy levels (good for onboarding)
        easiest = level_analysis.get('easiest_levels', [])
        if easiest:
            recommendations['positive_insights'].append({
                'achievement': 'Well-designed easy levels for onboarding',
                'insight': f'Levels {", ".join(easiest[:3])} have high completion rates',
                'recommendation': 'Use similar design principles for future early levels'
            })
        
        return recommendations
    
    def _calculate_priority_score(self, item: Dict, priority: str) -> int:
        """Calculate numeric priority score"""
        base_scores = {
            'critical': 100,
            'high_priority': 70,
            'medium_priority': 40,
            'low_priority': 10,
            'positive_insights': 0
        }
        
        score = base_scores.get(priority, 0)
        
        # Adjust based on impact metrics
        if 'impact' in item:
            score += 10
        if 'expected_improvement' in item:
            score += 15
        if 'players_stuck' in item.get('metrics', {}):
            stuck = item['metrics']['players_stuck']
            score += min(stuck // 10, 20)
        
        return score
