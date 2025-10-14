"""
Level Difficulty Analyzer
Analyzes level difficulty, completion rates, and player drop-off points
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from collections import defaultdict
from datetime import datetime, timedelta


class LevelAnalyzer:
    """
    Comprehensive level analytics and difficulty analysis
    
    Provides insights on:
    - Level completion rates
    - Average attempts per level
    - Time spent per level
    - Difficulty scoring
    - Drop-off points (where players quit)
    - Level progression funnels
    """
    
    def __init__(self):
        self.level_stats_cache = {}
        self.cache_timestamp = None
        self.cache_duration = timedelta(minutes=5)
    
    def analyze_all_levels(self, level_events: List[Dict]) -> Dict:
        """
        Comprehensive analysis of all levels
        
        Returns:
            {
                'level_stats': Dict[str, Dict],
                'difficulty_scores': Dict[str, float],
                'drop_off_levels': List[str],
                'bottleneck_levels': List[str],
                'easiest_levels': List[str],
                'hardest_levels': List[str]
            }
        """
        if not level_events:
            return self._empty_analysis()
        
        # Group events by level
        level_groups = defaultdict(list)
        for event in level_events:
            level_id = event.get('levelId', 'unknown')
            level_groups[level_id].append(event)
        
        # Calculate stats for each level
        level_stats = {}
        difficulty_scores = {}
        
        for level_id, events in level_groups.items():
            stats = self._calculate_level_stats(level_id, events)
            level_stats[level_id] = stats
            difficulty_scores[level_id] = stats['difficulty_score']
        
        # Identify problematic levels
        drop_off_levels = self._identify_drop_off_levels(level_stats)
        bottleneck_levels = self._identify_bottlenecks(level_stats)
        
        # Sort by difficulty
        sorted_by_difficulty = sorted(
            difficulty_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        hardest_levels = [lvl for lvl, _ in sorted_by_difficulty[:10]]
        easiest_levels = [lvl for lvl, _ in sorted_by_difficulty[-10:]]
        
        return {
            'level_stats': level_stats,
            'difficulty_scores': difficulty_scores,
            'drop_off_levels': drop_off_levels,
            'bottleneck_levels': bottleneck_levels,
            'easiest_levels': easiest_levels,
            'hardest_levels': hardest_levels,
            'total_levels_analyzed': len(level_stats)
        }
    
    def _calculate_level_stats(self, level_id: str, events: List[Dict]) -> Dict:
        """Calculate comprehensive statistics for a single level"""
        # Group by user to calculate attempts
        user_events = defaultdict(list)
        for event in events:
            user_id = event.get('globalParams', {}).get('userId', 'unknown')
            user_events[user_id].append(event)
        
        total_unique_players = len(user_events)
        total_attempts = len(events)
        
        # Calculate completion rate
        completed_events = [e for e in events if e.get('completed', False)]
        completion_count = len(set(
            e.get('globalParams', {}).get('userId') 
            for e in completed_events
        ))
        completion_rate = completion_count / total_unique_players if total_unique_players > 0 else 0
        
        # Average attempts to complete
        attempts_to_complete = []
        for user_id, user_level_events in user_events.items():
            # Sort by timestamp
            sorted_events = sorted(
                user_level_events, 
                key=lambda e: e.get('globalParams', {}).get('timestamp', '')
            )
            
            # Count attempts until first completion
            for idx, event in enumerate(sorted_events, 1):
                if event.get('completed', False):
                    attempts_to_complete.append(idx)
                    break
        
        avg_attempts = np.mean(attempts_to_complete) if attempts_to_complete else 0
        
        # Time statistics
        durations = [
            e.get('levelDuration', 0) / 1000  # Convert to seconds
            for e in events 
            if e.get('levelDuration')
        ]
        avg_time = np.mean(durations) if durations else 0
        median_time = np.median(durations) if durations else 0
        
        # Score statistics
        scores = [e.get('score', 0) for e in completed_events if e.get('score')]
        avg_score = np.mean(scores) if scores else 0
        
        # Stars earned
        stars = [e.get('starsEarned', 0) for e in completed_events if e.get('starsEarned')]
        avg_stars = np.mean(stars) if stars else 0
        
        # Perfect completions
        perfect_count = len([e for e in completed_events if e.get('perfectCompletion', False)])
        perfect_rate = perfect_count / completion_count if completion_count > 0 else 0
        
        # Fail reasons
        fail_reasons = defaultdict(int)
        for event in events:
            if not event.get('completed', False):
                reason = event.get('failReason', 'unknown')
                if reason:
                    fail_reasons[reason] += 1
        
        # Calculate difficulty score (0-100, higher = harder)
        difficulty_score = self._calculate_difficulty_score(
            completion_rate,
            avg_attempts,
            avg_time,
            perfect_rate
        )
        
        return {
            'level_id': level_id,
            'total_unique_players': total_unique_players,
            'total_attempts': total_attempts,
            'completion_count': completion_count,
            'completion_rate': round(completion_rate, 3),
            'avg_attempts_to_complete': round(avg_attempts, 2),
            'avg_time_seconds': round(avg_time, 1),
            'median_time_seconds': round(median_time, 1),
            'avg_score': round(avg_score, 1),
            'avg_stars_earned': round(avg_stars, 2),
            'perfect_completion_rate': round(perfect_rate, 3),
            'difficulty_score': round(difficulty_score, 1),
            'top_fail_reasons': dict(sorted(fail_reasons.items(), key=lambda x: x[1], reverse=True)[:5])
        }
    
    def _calculate_difficulty_score(
        self, 
        completion_rate: float, 
        avg_attempts: float, 
        avg_time: float,
        perfect_rate: float
    ) -> float:
        """
        Calculate difficulty score (0-100)
        
        Components:
        - Low completion rate → higher difficulty
        - More attempts needed → higher difficulty  
        - Longer time → higher difficulty
        - Low perfect rate → higher difficulty
        """
        # Invert completion rate (low completion = high difficulty)
        completion_component = (1 - completion_rate) * 40
        
        # Attempts component (normalized, capped at 10 attempts)
        attempts_component = min(avg_attempts / 10, 1) * 30
        
        # Time component (normalized, capped at 10 minutes)
        time_component = min(avg_time / 600, 1) * 20
        
        # Perfect rate component
        perfect_component = (1 - perfect_rate) * 10
        
        difficulty = completion_component + attempts_component + time_component + perfect_component
        
        return min(difficulty, 100)
    
    def _identify_drop_off_levels(self, level_stats: Dict) -> List[Dict]:
        """Identify levels where players are dropping off"""
        drop_offs = []
        
        for level_id, stats in level_stats.items():
            # High drop-off indicators:
            # 1. Low completion rate
            # 2. High number of players who tried
            # 3. High difficulty score
            
            if (stats['completion_rate'] < 0.5 and 
                stats['total_unique_players'] > 10 and
                stats['difficulty_score'] > 60):
                
                drop_offs.append({
                    'level_id': level_id,
                    'completion_rate': stats['completion_rate'],
                    'players_stuck': stats['total_unique_players'] - stats['completion_count'],
                    'difficulty_score': stats['difficulty_score'],
                    'severity': 'critical' if stats['completion_rate'] < 0.3 else 'high'
                })
        
        # Sort by severity
        drop_offs.sort(key=lambda x: x['completion_rate'])
        
        return drop_offs[:15]  # Top 15 problematic levels
    
    def _identify_bottlenecks(self, level_stats: Dict) -> List[Dict]:
        """Identify bottleneck levels (high traffic, high failure)"""
        bottlenecks = []
        
        # Sort by total attempts to find high-traffic levels
        sorted_levels = sorted(
            level_stats.items(),
            key=lambda x: x[1]['total_attempts'],
            reverse=True
        )
        
        for level_id, stats in sorted_levels[:20]:  # Top 20 by traffic
            if stats['completion_rate'] < 0.6:
                bottlenecks.append({
                    'level_id': level_id,
                    'total_attempts': stats['total_attempts'],
                    'completion_rate': stats['completion_rate'],
                    'avg_attempts': stats['avg_attempts_to_complete'],
                    'impact_score': stats['total_attempts'] * (1 - stats['completion_rate'])
                })
        
        # Sort by impact score
        bottlenecks.sort(key=lambda x: x['impact_score'], reverse=True)
        
        return bottlenecks[:10]
    
    def get_level_progression_funnel(self, level_events: List[Dict]) -> Dict:
        """
        Analyze player progression through levels
        Shows how many players reach each level number
        """
        # Extract level numbers
        level_numbers = {}
        for event in level_events:
            level_num = event.get('levelNumber', 0)
            user_id = event.get('globalParams', {}).get('userId', 'unknown')
            
            if level_num > 0:
                if level_num not in level_numbers:
                    level_numbers[level_num] = set()
                level_numbers[level_num].add(user_id)
        
        # Create funnel
        funnel = []
        sorted_levels = sorted(level_numbers.items())
        
        for level_num, users in sorted_levels:
            funnel.append({
                'level_number': level_num,
                'players_reached': len(users),
                'retention_rate': len(users) / len(level_numbers.get(1, {1})) if 1 in level_numbers else 0
            })
        
        # Calculate drop-off between levels
        for i in range(len(funnel) - 1):
            current_players = funnel[i]['players_reached']
            next_players = funnel[i + 1]['players_reached']
            drop_off = current_players - next_players
            drop_off_rate = drop_off / current_players if current_players > 0 else 0
            funnel[i]['drop_off_to_next'] = drop_off
            funnel[i]['drop_off_rate'] = round(drop_off_rate, 3)
        
        return {
            'funnel': funnel,
            'total_levels_in_funnel': len(funnel),
            'biggest_drop_off': max(funnel, key=lambda x: x.get('drop_off_rate', 0)) if funnel else None
        }
    
    def get_level_time_analysis(self, level_events: List[Dict]) -> Dict:
        """Analyze time spent on each level"""
        level_times = defaultdict(list)
        
        for event in level_events:
            level_id = event.get('levelId', 'unknown')
            duration = event.get('levelDuration', 0) / 1000  # Convert to seconds
            if duration > 0:
                level_times[level_id].append(duration)
        
        time_analysis = {}
        for level_id, times in level_times.items():
            time_analysis[level_id] = {
                'avg_time': round(np.mean(times), 1),
                'median_time': round(np.median(times), 1),
                'min_time': round(min(times), 1),
                'max_time': round(max(times), 1),
                'std_dev': round(np.std(times), 1),
                'total_playtime': round(sum(times), 1)
            }
        
        # Find levels with unusual time patterns
        avg_times = [stats['avg_time'] for stats in time_analysis.values()]
        if avg_times:
            mean_time = np.mean(avg_times)
            std_time = np.std(avg_times)
            
            unusually_long = [
                {'level_id': lvl, 'avg_time': stats['avg_time']}
                for lvl, stats in time_analysis.items()
                if stats['avg_time'] > mean_time + 2 * std_time
            ]
            
            unusually_short = [
                {'level_id': lvl, 'avg_time': stats['avg_time']}
                for lvl, stats in time_analysis.items()
                if stats['avg_time'] < mean_time - std_time and stats['avg_time'] > 10
            ]
        else:
            unusually_long = []
            unusually_short = []
        
        return {
            'level_times': time_analysis,
            'unusually_long_levels': sorted(unusually_long, key=lambda x: x['avg_time'], reverse=True)[:10],
            'unusually_short_levels': sorted(unusually_short, key=lambda x: x['avg_time'])[:10]
        }
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            'level_stats': {},
            'difficulty_scores': {},
            'drop_off_levels': [],
            'bottleneck_levels': [],
            'easiest_levels': [],
            'hardest_levels': [],
            'total_levels_analyzed': 0
        }
