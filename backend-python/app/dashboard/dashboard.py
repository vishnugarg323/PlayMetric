"""
PAIME Dashboard - Beautiful Analytics Dashboard
Built with Plotly Dash
"""
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import pandas as pd
from typing import Dict, List

# Initialize Dash app with dark theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    title="PAIME - Game Analytics Dashboard"
)

# API base URL - configurable for Railway deployment
import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Custom color scheme
COLORS = {
    'background': '#060606',
    'card_bg': '#1a1a1a',
    'text': '#ffffff',
    'primary': '#00d9ff',
    'success': '#00ff88',
    'warning': '#ffaa00',
    'danger': '#ff4444',
    'info': '#8844ff',
    'grid': '#333333'
}

# Helper functions
def fetch_api_data(endpoint: str) -> Dict:
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return {}


def create_metric_card(title: str, value: str, subtitle: str = "", color: str = COLORS['primary']):
    """Create a metric display card"""
    return dbc.Card([
        dbc.CardBody([
            html.H6(title, className="text-muted mb-2"),
            html.H2(value, style={'color': color, 'fontWeight': 'bold'}),
            html.P(subtitle, className="text-muted mb-0", style={'fontSize': '0.9rem'})
        ])
    ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})


def create_section_header(title: str, icon: str = "📊"):
    """Create a section header"""
    return html.Div([
        html.H3([icon + " " + title], 
                style={'color': COLORS['primary'], 'marginTop': '30px', 'marginBottom': '20px'})
    ])


# Dashboard Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🎮 PAIME", style={
                    'color': COLORS['primary'],
                    'fontWeight': 'bold',
                    'fontSize': '3rem',
                    'marginBottom': '0'
                }),
                html.P("PlayMetric AI Metrics Engine", style={
                    'color': COLORS['text'],
                    'fontSize': '1.2rem',
                    'opacity': '0.8'
                }),
                html.P("Real-time Game Analytics & AI Insights", style={
                    'color': COLORS['text'],
                    'fontSize': '0.9rem',
                    'opacity': '0.6'
                })
            ], style={'textAlign': 'center', 'padding': '20px 0'})
        ])
    ]),
    
    # Refresh Button
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button(
                    [html.I(className="fas fa-sync-alt"), " Refresh Data"],
                    id='refresh-button',
                    color='primary',
                    size='lg',
                    style={'marginBottom': '20px'}
                ),
                html.Span(id='last-refresh-time', style={'marginLeft': '20px', 'color': COLORS['text'], 'opacity': '0.7'})
            ], style={'textAlign': 'center'})
        ])
    ]),
    
    # Hidden div to store refresh trigger
    html.Div(id='refresh-trigger', style={'display': 'none'}),
    
    # Key Metrics Row
    create_section_header("📈 Key Metrics", "📈"),
    html.Div(id='key-metrics-row'),
    
    # User Activity Charts
    create_section_header("👥 User Activity", "👥"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("User Activity Trends", className="card-title"),
                    dcc.Graph(id='user-activity-chart')
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Platform Distribution", className="card-title"),
                    dcc.Graph(id='platform-distribution-chart')
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
        ], md=6),
    ], className="mb-4"),
    
    # Level Analysis
    create_section_header("🎯 Level Analysis", "🎯"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Level Difficulty Heatmap", className="card-title"),
                    dcc.Graph(id='level-difficulty-heatmap')
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
        ], md=12),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Level Progression Funnel", className="card-title"),
                    dcc.Graph(id='level-funnel-chart')
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Drop-off Levels", className="card-title"),
                    html.Div(id='dropoff-levels-list')
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
        ], md=6),
    ], className="mb-4"),
    
    # Churn Analysis
    create_section_header("⚠️ Churn Risk Analysis", "⚠️"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Churn Risk Distribution", className="card-title"),
                    dcc.Graph(id='churn-risk-chart')
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("High-Risk Users", className="card-title"),
                    html.Div(id='high-risk-users-list')
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
        ], md=6),
    ], className="mb-4"),
    
    # AI Recommendations
    create_section_header("💡 AI Recommendations", "💡"),
    html.Div(id='ai-recommendations'),
    
    # Comprehensive AI Insights
    create_section_header("🤖 Advanced AI Insights", "🤖"),
    html.Div(id='ai-comprehensive-insights'),
    
    # Footer
    html.Hr(style={'borderColor': COLORS['grid'], 'marginTop': '40px'}),
    html.P("PAIME - PlayMetric AI Metrics Engine v1.0 | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           style={'textAlign': 'center', 'color': COLORS['text'], 'opacity': '0.6', 'padding': '20px'})
    
], fluid=True, style={'backgroundColor': COLORS['background'], 'minHeight': '100vh', 'padding': '20px'})


# Callbacks
@callback(
    Output('refresh-trigger', 'children'),
    Output('last-refresh-time', 'children'),
    Input('refresh-button', 'n_clicks'),
    prevent_initial_call=False
)
def trigger_refresh(n_clicks):
    """Trigger data refresh and update timestamp"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(n_clicks or 0), f"Last refreshed: {now}"

@callback(
    Output('key-metrics-row', 'children'),
    Input('refresh-trigger', 'children')
)
def update_key_metrics(trigger):
    """Update key metrics cards"""
    overview = fetch_api_data('/analytics/overview')
    
    if not overview:
        return html.Div("Loading...", className="text-center")
    
    user_metrics = overview.get('user_metrics', {})
    session_metrics = overview.get('session_metrics', {})
    revenue_metrics = overview.get('revenue_metrics', {})
    retention = overview.get('retention_rates', {})
    
    return dbc.Row([
        dbc.Col([
            create_metric_card(
                "Total Users",
                f"{user_metrics.get('total_users', 0):,}",
                f"DAU: {user_metrics.get('dau', 0)} | MAU: {user_metrics.get('mau', 0)}",
                COLORS['primary']
            )
        ], md=2),
        dbc.Col([
            create_metric_card(
                "Active Users Today",
                f"{user_metrics.get('dau', 0):,}",
                f"DAU/MAU: {user_metrics.get('dau_mau_ratio', 0):.1%}",
                COLORS['success']
            )
        ], md=2),
        dbc.Col([
            create_metric_card(
                "Avg Session",
                f"{session_metrics.get('avg_session_duration_minutes', 0):.1f}m",
                f"Total: {session_metrics.get('total_playtime_hours', 0):.1f}h",
                COLORS['info']
            )
        ], md=2),
        dbc.Col([
            create_metric_card(
                "Revenue",
                f"${revenue_metrics.get('total_revenue', 0):.2f}",
                f"{revenue_metrics.get('paying_users', 0)} payers",
                COLORS['warning']
            )
        ], md=2),
        dbc.Col([
            create_metric_card(
                "Day 1 Retention",
                f"{retention.get('day_1_retention', 0):.1f}%",
                f"Day 7: {retention.get('day_7_retention', 0):.1f}%",
                COLORS['success'] if retention.get('day_1_retention', 0) > 50 else COLORS['warning']
            )
        ], md=2),
        dbc.Col([
            create_metric_card(
                "Total Events",
                f"{overview.get('total_events_tracked', 0):,}",
                f"Sessions: {session_metrics.get('total_sessions', 0)}",
                COLORS['primary']
            )
        ], md=2),
    ], className="mb-4")


@callback(
    Output('user-activity-chart', 'figure'),
    Input('refresh-trigger', 'children')
)
def update_user_activity(trigger):
    """Update user activity trend chart"""
    overview = fetch_api_data('/analytics/overview')
    
    if not overview:
        return go.Figure()
    
    user_metrics = overview.get('user_metrics', {})
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['DAU', 'WAU', 'MAU'],
        y=[user_metrics.get('dau', 0), user_metrics.get('wau', 0), user_metrics.get('mau', 0)],
        marker_color=[COLORS['success'], COLORS['info'], COLORS['primary']],
        text=[user_metrics.get('dau', 0), user_metrics.get('wau', 0), user_metrics.get('mau', 0)],
        textposition='auto',
    ))
    
    fig.update_layout(
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text']),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=300
    )
    
    return fig


@callback(
    Output('platform-distribution-chart', 'figure'),
    Input('refresh-trigger', 'children')
)
def update_platform_distribution(trigger):
    """Update platform distribution pie chart"""
    overview = fetch_api_data('/analytics/overview')
    
    if not overview:
        return go.Figure()
    
    platform_dist = overview.get('platform_distribution', {})
    
    labels = list(platform_dist.keys())
    values = [platform_dist[p]['count'] for p in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=[COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['info']])
    )])
    
    fig.update_layout(
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        height=300,
        showlegend=True
    )
    
    return fig


@callback(
    Output('level-difficulty-heatmap', 'figure'),
    Input('refresh-trigger', 'children')
)
def update_level_difficulty(trigger):
    """Update level difficulty heatmap"""
    level_data = fetch_api_data('/analytics/levels')
    
    if not level_data or not level_data.get('level_stats'):
        return go.Figure()
    
    level_stats = level_data.get('level_stats', {})
    
    # Prepare data for heatmap
    levels = list(level_stats.keys())[:30]  # Top 30 levels
    metrics = ['Completion Rate', 'Difficulty Score', 'Avg Attempts']
    
    z_data = []
    for metric in metrics:
        row = []
        for level in levels:
            stats = level_stats[level]
            if metric == 'Completion Rate':
                row.append(stats.get('completion_rate', 0) * 100)
            elif metric == 'Difficulty Score':
                row.append(stats.get('difficulty_score', 0))
            elif metric == 'Avg Attempts':
                row.append(min(stats.get('avg_attempts_to_complete', 0), 10))  # Cap at 10
        z_data.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=levels,
        y=metrics,
        colorscale=[[0, COLORS['success']], [0.5, COLORS['warning']], [1, COLORS['danger']]],
        text=[[f"{val:.1f}" for val in row] for row in z_data],
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Score")
    ))
    
    fig.update_layout(
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text']),
        margin=dict(l=100, r=40, t=40, b=100),
        height=300,
        xaxis=dict(tickangle=-45)
    )
    
    return fig


@callback(
    Output('level-funnel-chart', 'figure'),
    Input('refresh-trigger', 'children')
)
def update_level_funnel(trigger):
    """Update level progression funnel"""
    level_data = fetch_api_data('/analytics/levels')
    
    if not level_data or not level_data.get('level_progression_funnel'):
        return go.Figure()
    
    funnel = level_data.get('level_progression_funnel', {}).get('funnel', [])
    
    if not funnel:
        return go.Figure()
    
    # Take first 15 levels for clarity
    funnel = funnel[:15]
    
    levels = [f"Level {f['level_number']}" for f in funnel]
    players = [f['players_reached'] for f in funnel]
    
    fig = go.Figure(go.Funnel(
        y=levels,
        x=players,
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=COLORS['primary'])
    ))
    
    fig.update_layout(
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text']),
        margin=dict(l=120, r=40, t=40, b=40),
        height=500
    )
    
    return fig


@callback(
    Output('dropoff-levels-list', 'children'),
    Input('refresh-trigger', 'children')
)
def update_dropoff_levels(trigger):
    """Update drop-off levels list"""
    level_data = fetch_api_data('/analytics/levels')
    
    if not level_data or not level_data.get('drop_off_levels'):
        return html.P("No data available", className="text-muted")
    
    dropoffs = level_data.get('drop_off_levels', [])[:10]
    
    if not dropoffs:
        return html.P("✅ No significant drop-off levels detected!", 
                     style={'color': COLORS['success'], 'padding': '20px'})
    
    items = []
    for level in dropoffs:
        severity_color = COLORS['danger'] if level['severity'] == 'critical' else COLORS['warning']
        items.append(
            dbc.ListGroupItem([
                html.Div([
                    html.Span(level['level_id'], style={'fontWeight': 'bold', 'fontSize': '1.1rem'}),
                    html.Span(f" {level['severity'].upper()}", 
                             style={'color': severity_color, 'marginLeft': '10px', 'fontSize': '0.8rem'}),
                ]),
                html.Small(f"Completion: {level['completion_rate']:.1%} | "
                          f"{level['players_stuck']} players stuck | "
                          f"Difficulty: {level['difficulty_score']:.1f}/100",
                          className="text-muted")
            ], style={'backgroundColor': COLORS['card_bg'], 'border': '1px solid ' + COLORS['grid']})
        )
    
    return dbc.ListGroup(items)


@callback(
    Output('churn-risk-chart', 'figure'),
    Input('refresh-trigger', 'children')
)
def update_churn_risk(trigger):
    """Update churn risk distribution"""
    churn_data = fetch_api_data('/analytics/churn?limit=50')
    
    if not churn_data:
        return go.Figure()
    
    risk_dist = churn_data.get('risk_distribution', {})
    
    fig = go.Figure(data=[go.Bar(
        x=['Low', 'Medium', 'High', 'Critical'],
        y=[risk_dist.get('low', 0), risk_dist.get('medium', 0), 
           risk_dist.get('high', 0), risk_dist.get('critical', 0)],
        marker_color=[COLORS['success'], COLORS['info'], COLORS['warning'], COLORS['danger']],
        text=[risk_dist.get('low', 0), risk_dist.get('medium', 0), 
              risk_dist.get('high', 0), risk_dist.get('critical', 0)],
        textposition='auto',
    )])
    
    fig.update_layout(
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text']),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=300,
        yaxis=dict(title="Number of Users")
    )
    
    return fig


@callback(
    Output('high-risk-users-list', 'children'),
    Input('refresh-trigger', 'children')
)
def update_high_risk_users(trigger):
    """Update high-risk users list"""
    churn_data = fetch_api_data('/analytics/churn?limit=100')
    
    if not churn_data:
        return html.P("Loading...", className="text-muted")
    
    predictions = churn_data.get('churn_predictions', [])
    high_risk = [p for p in predictions if p['churn_risk'] in ['high', 'critical']][:10]
    
    if not high_risk:
        return html.P("✅ No high-risk users detected!", 
                     style={'color': COLORS['success'], 'padding': '20px'})
    
    items = []
    for user in high_risk:
        risk_color = COLORS['danger'] if user['churn_risk'] == 'critical' else COLORS['warning']
        items.append(
            dbc.ListGroupItem([
                html.Div([
                    html.Span(user['user_id'], style={'fontWeight': 'bold'}),
                    html.Span(f" {user['churn_risk'].upper()}", 
                             style={'color': risk_color, 'marginLeft': '10px', 'fontSize': '0.8rem'}),
                ]),
                html.Small(f"Churn Probability: {user['churn_probability']:.1%} | "
                          f"Platform: {user['platform']} | "
                          f"Sessions: {user['total_sessions']}",
                          className="text-muted"),
                html.Small(html.Br()),
                html.Small(f"Risk: {', '.join(user.get('risk_factors', []))[:100]}...",
                          className="text-muted", style={'fontSize': '0.75rem'})
            ], style={'backgroundColor': COLORS['card_bg'], 'border': '1px solid ' + COLORS['grid']})
        )
    
    return dbc.ListGroup(items)


@callback(
    Output('ai-recommendations', 'children'),
    Input('refresh-trigger', 'children')
)
def update_recommendations(trigger):
    """Update AI recommendations"""
    recommendations = fetch_api_data('/analytics/recommendations')
    
    if not recommendations:
        return html.P("Loading recommendations...", className="text-muted")
    
    sections = []
    
    # Critical issues
    if recommendations.get('critical'):
        items = []
        for rec in recommendations['critical']:
            items.append(
                dbc.Card([
                    dbc.CardBody([
                        html.H6([
                            "🚨 ", rec.get('category', 'General'), ": ", rec.get('issue', '')
                        ], style={'color': COLORS['danger']}),
                        html.P(rec.get('impact', ''), className="text-muted mb-2"),
                        html.P("Recommendations:", style={'fontWeight': 'bold', 'marginTop': '10px', 'marginBottom': '5px'}),
                        html.Ul([html.Li(r) for r in rec.get('recommendations', [])], 
                               style={'fontSize': '0.9rem'}),
                        html.Small(f"Expected: {rec.get('expected_improvement', 'N/A')}", 
                                  style={'color': COLORS['success']}) if 'expected_improvement' in rec else None
                    ])
                ], style={'backgroundColor': COLORS['card_bg'], 'border': f'2px solid {COLORS["danger"]}', 
                         'marginBottom': '15px'})
            )
        sections.append(html.Div([
            html.H4("🚨 Critical Issues", style={'color': COLORS['danger'], 'marginBottom': '15px'}),
            html.Div(items)
        ]))
    
    # High priority
    if recommendations.get('high_priority'):
        items = []
        for rec in recommendations['high_priority'][:5]:  # Top 5
            items.append(
                dbc.Card([
                    dbc.CardBody([
                        html.H6([
                            "⚠️ ", rec.get('category', 'General'), ": ", rec.get('issue', '')
                        ], style={'color': COLORS['warning']}),
                        html.Ul([html.Li(r) for r in rec.get('recommendations', [])[:3]], 
                               style={'fontSize': '0.9rem'})
                    ])
                ], style={'backgroundColor': COLORS['card_bg'], 'border': f'1px solid {COLORS["warning"]}', 
                         'marginBottom': '10px'})
            )
        sections.append(html.Div([
            html.H4("⚠️ High Priority", style={'color': COLORS['warning'], 'marginTop': '20px', 'marginBottom': '15px'}),
            html.Div(items)
        ]))
    
    # Positive insights
    if recommendations.get('positive_insights'):
        items = []
        for rec in recommendations['positive_insights']:
            items.append(
                dbc.ListGroupItem([
                    html.Div([
                        html.Span("✅ ", style={'fontSize': '1.2rem'}),
                        html.Span(rec.get('achievement', ''), style={'fontWeight': 'bold'})
                    ]),
                    html.Small(rec.get('insight', ''), className="text-muted")
                ], style={'backgroundColor': COLORS['card_bg'], 'border': f'1px solid {COLORS["success"]}'})
            )
        sections.append(html.Div([
            html.H4("✅ What's Working Well", style={'color': COLORS['success'], 'marginTop': '20px', 'marginBottom': '15px'}),
            dbc.ListGroup(items)
        ]))
    
    return html.Div(sections) if sections else html.P("No recommendations at this time", className="text-center text-muted")


@callback(
    Output('ai-comprehensive-insights', 'children'),
    Input('refresh-trigger', 'children')
)
def update_ai_insights(trigger):
    """Update comprehensive AI insights"""
    insights = fetch_api_data('/analytics/ai-insights')
    
    if not insights or 'timestamp' not in insights:
        return html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        dbc.Spinner(color="primary"),
                        html.P("Analyzing data with AI...", className="text-center mt-3")
                    ], style={'textAlign': 'center', 'padding': '40px'})
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
        ])
    
    sections = []
    
    # Executive Summary
    if insights.get('executive_summary'):
        summary = insights['executive_summary']
        health_status = summary.get('health_status', 'unknown')
        
        status_colors = {
            'healthy': COLORS['success'],
            'warning': COLORS['warning'],
            'critical': COLORS['danger']
        }
        status_color = status_colors.get(health_status, COLORS['info'])
        
        sections.append(dbc.Card([
            dbc.CardBody([
                html.H4([
                    "📊 Executive Summary",
                    html.Span(
                        f" {health_status.upper()}",
                        style={
                            'color': status_color,
                            'marginLeft': '20px',
                            'fontSize': '1.2rem',
                            'fontWeight': 'bold'
                        }
                    )
                ]),
                html.Hr(style={'borderColor': COLORS['grid']}),
                
                # Top Priorities
                html.Div([
                    html.H6("🎯 Top Priorities", style={'marginTop': '15px'}),
                    html.Ul([
                        html.Li(f"{p['priority']}: {p['action']}")
                        for p in summary.get('top_priorities', [])
                    ] if summary.get('top_priorities') else [html.Li("All systems operating normally")])
                ]),
                
                # Best Opportunity
                html.Div([
                    html.H6("💎 Best Opportunity", style={'marginTop': '15px'}),
                    html.P(
                        f"{summary.get('key_metrics', {}).get('best_opportunity', {}).get('area', 'N/A')} "
                        f"(Score: {summary.get('key_metrics', {}).get('best_opportunity', {}).get('score', 0)})"
                    ) if summary.get('key_metrics', {}).get('best_opportunity') else html.P("Analyzing...")
                ]),
                
                # Quick Wins
                html.Div([
                    html.H6("⚡ Quick Wins", style={'marginTop': '15px'}),
                    html.Ul([
                        html.Li(win) for win in summary.get('quick_wins', [])
                    ] if summary.get('quick_wins') else [html.Li("No quick wins identified yet")])
                ])
            ])
        ], style={'backgroundColor': COLORS['card_bg'], 'border': f'2px solid {status_color}', 'marginBottom': '20px'}))
    
    # Player Behavior Analysis
    if insights.get('player_behavior_analysis'):
        behavior = insights['player_behavior_analysis']
        
        behavior_cards = []
        
        # Session Patterns
        if behavior.get('session_patterns'):
            session = behavior['session_patterns']
            dist = session.get('distribution', {})
            
            session_types = list(dist.keys())
            session_counts = [dist[k]['count'] for k in session_types]
            
            fig = go.Figure(data=[go.Pie(
                labels=[k.title() for k in session_types],
                values=session_counts,
                hole=0.4,
                marker=dict(colors=[COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['info']])
            )])
            
            fig.update_layout(
                paper_bgcolor=COLORS['card_bg'],
                plot_bgcolor=COLORS['card_bg'],
                font=dict(color=COLORS['text']),
                margin=dict(l=40, r=40, t=40, b=40),
                height=300
            )
            
            behavior_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Session Type Distribution"),
                            dcc.Graph(figure=fig, config={'displayModeBar': False}),
                            html.Small(
                                f"Avg: {session.get('avg_duration_minutes', 0):.1f} min | "
                                f"Median: {session.get('median_duration_minutes', 0):.1f} min",
                                className="text-muted"
                            )
                        ])
                    ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
                ], md=6)
            )
        
        # Peak Hours
        if behavior.get('peak_activity_hours'):
            peak = behavior['peak_activity_hours']
            
            if peak.get('hourly_distribution'):
                hours = sorted(peak['hourly_distribution'].keys())
                counts = [peak['hourly_distribution'][h] for h in hours]
                
                fig = go.Figure(data=[go.Bar(
                    x=[f"{h:02d}:00" for h in hours],
                    y=counts,
                    marker_color=COLORS['primary']
                )])
                
                fig.update_layout(
                    paper_bgcolor=COLORS['card_bg'],
                    plot_bgcolor=COLORS['card_bg'],
                    font=dict(color=COLORS['text']),
                    margin=dict(l=40, r=40, t=40, b=40),
                    height=300,
                    xaxis_title="Hour of Day",
                    yaxis_title="Activity"
                )
                
                behavior_cards.append(
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Peak Activity Hours"),
                                dcc.Graph(figure=fig, config={'displayModeBar': False}),
                                html.Small(
                                    f"Peak: {peak.get('peak_hour', 0):02d}:00 with {peak.get('peak_hour_activity', 0)} events",
                                    className="text-muted"
                                )
                            ])
                        ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
                    ], md=6)
                )
        
        # Lifecycle Distribution
        if behavior.get('lifecycle_distribution'):
            lifecycle = behavior['lifecycle_distribution']
            
            stages = list(lifecycle.keys())
            counts = [lifecycle[s]['count'] for s in stages]
            percentages = [lifecycle[s]['percentage'] for s in stages]
            
            fig = go.Figure(data=[go.Bar(
                x=[s.replace('_', ' ').title() for s in stages],
                y=counts,
                text=[f"{p:.1f}%" for p in percentages],
                textposition='auto',
                marker_color=[COLORS['success'], COLORS['info'], COLORS['primary'], COLORS['warning'], COLORS['danger']]
            )])
            
            fig.update_layout(
                paper_bgcolor=COLORS['card_bg'],
                plot_bgcolor=COLORS['card_bg'],
                font=dict(color=COLORS['text']),
                margin=dict(l=40, r=40, t=40, b=40),
                height=300,
                xaxis_title="Lifecycle Stage",
                yaxis_title="Users"
            )
            
            behavior_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Player Lifecycle Distribution"),
                            dcc.Graph(figure=fig, config={'displayModeBar': False})
                        ])
                    ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none'})
                ], md=12)
            )
        
        # Key Findings
        if behavior.get('key_findings'):
            behavior_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("🔍 Key Behavior Findings"),
                            html.Ul([
                                html.Li(finding, style={'marginBottom': '8px'})
                                for finding in behavior['key_findings']
                            ])
                        ])
                    ], style={'backgroundColor': COLORS['card_bg'], 'border': f'1px solid {COLORS["info"]}'})
                ], md=12)
            )
        
        sections.append(html.Div([
            html.H5("👥 Player Behavior Analysis", style={'color': COLORS['primary'], 'marginBottom': '15px'}),
            dbc.Row(behavior_cards, className="mb-4")
        ]))
    
    # Revenue Optimization
    if insights.get('revenue_optimization'):
        revenue = insights['revenue_optimization']
        
        revenue_cards = []
        
        # Key Metrics
        revenue_cards.append(
            dbc.Col([
                create_metric_card(
                    "Conversion Rate",
                    f"{revenue.get('conversion_rate', 0):.2f}%",
                    f"{revenue.get('total_payers', 0)} payers",
                    COLORS['warning']
                )
            ], md=3)
        )
        
        revenue_cards.append(
            dbc.Col([
                create_metric_card(
                    "Avg Transaction",
                    f"${revenue.get('avg_transaction_value', 0):.2f}",
                    "per purchase",
                    COLORS['success']
                )
            ], md=3)
        )
        
        revenue_cards.append(
            dbc.Col([
                create_metric_card(
                    "Whale Candidates",
                    str(len(revenue.get('whale_candidates', []))),
                    "high-potential users",
                    COLORS['info']
                )
            ], md=3)
        )
        
        # Recommendations
        if revenue.get('recommendations'):
            revenue_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("💰 Revenue Recommendations"),
                            html.Ul([
                                html.Li(rec, style={'fontSize': '0.9rem', 'marginBottom': '8px'})
                                for rec in revenue['recommendations']
                            ])
                        ])
                    ], style={'backgroundColor': COLORS['card_bg'], 'border': f'1px solid {COLORS["warning"]}'})
                ], md=12)
            )
        
        sections.append(html.Div([
            html.H5("💰 Revenue Optimization", style={'color': COLORS['primary'], 'marginTop': '20px', 'marginBottom': '15px'}),
            dbc.Row(revenue_cards, className="mb-4")
        ]))
    
    # Engagement Predictions
    if insights.get('engagement_predictions'):
        pred = insights['engagement_predictions']
        
        trend_icon = '📈' if pred.get('trend_direction') == 'growing' else '📉' if pred.get('trend_direction') == 'declining' else '➡️'
        trend_color = COLORS['success'] if pred.get('trend_direction') == 'growing' else COLORS['danger'] if pred.get('trend_direction') == 'declining' else COLORS['info']
        
        sections.append(html.Div([
            html.H5("📊 Engagement Predictions", style={'color': COLORS['primary'], 'marginTop': '20px', 'marginBottom': '15px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("7-Day Trend"),
                            html.Div([
                                html.H3([
                                    trend_icon + " ",
                                    pred.get('trend_direction', 'stable').upper()
                                ], style={'color': trend_color, 'marginBottom': '10px'}),
                                html.P(f"{pred.get('trend_percentage', 0):+.1f}% change", 
                                      style={'fontSize': '1.2rem', 'color': trend_color}),
                                html.Hr(style={'borderColor': COLORS['grid']}),
                                html.Small(f"Recent 7 days: {pred.get('recent_7_days_events', 0):,} events", 
                                          className="text-muted d-block"),
                                html.Small(f"Previous 7 days: {pred.get('previous_7_days_events', 0):,} events", 
                                          className="text-muted d-block"),
                                html.Small(f"Projected next 7 days: {pred.get('projected_next_7_days', 0):,} events", 
                                          style={'color': COLORS['info']}, className="d-block mt-2"),
                                html.Small(f"Confidence: {pred.get('confidence', 'medium')}", 
                                          className="text-muted d-block mt-2")
                            ])
                        ])
                    ], style={'backgroundColor': COLORS['card_bg'], 'border': f'2px solid {trend_color}'})
                ], md=6)
            ], className="mb-4")
        ]))
    
    # ML Player Segmentation
    if insights.get('player_segments_ml') and insights['player_segments_ml'].get('status') == 'success':
        segments = insights['player_segments_ml']
        
        segment_cards = []
        for seg_id, seg_data in segments.get('segments', {}).items():
            segment_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6(seg_data['name'], style={'color': COLORS['primary']}),
                            html.P(f"{seg_data['size']} users", className="text-muted"),
                            html.Hr(style={'borderColor': COLORS['grid']}),
                            html.Small(f"Avg Sessions: {seg_data['avg_sessions']:.1f}", className="d-block"),
                            html.Small(f"Avg Events: {seg_data['avg_events']:.1f}", className="d-block"),
                            html.Small(f"Avg Spending: ${seg_data['avg_spending']:.2f}", className="d-block"),
                            html.Small(f"Daily Activity: {seg_data['avg_daily_activity']:.1f}", className="d-block")
                        ])
                    ], style={'backgroundColor': COLORS['card_bg'], 'border': '1px solid ' + COLORS['grid']})
                ], md=3)
            )
        
        sections.append(html.Div([
            html.H5("🤖 ML-Based Player Segmentation", 
                   style={'color': COLORS['primary'], 'marginTop': '20px', 'marginBottom': '15px'}),
            dbc.Row(segment_cards, className="mb-4")
        ]))
    
    # Opportunity Scores
    if insights.get('opportunity_score'):
        opp = insights['opportunity_score']
        
        opportunities = [
            {'name': 'Monetization', 'score': opp.get('monetization', 0), 'icon': '💰'},
            {'name': 'Engagement', 'score': opp.get('engagement', 0), 'icon': '🎮'},
            {'name': 'Retention', 'score': opp.get('retention', 0), 'icon': '🔄'},
            {'name': 'Growth', 'score': opp.get('growth', 0), 'icon': '📈'}
        ]
        
        opp_cards = []
        for opportunity in opportunities:
            score = opportunity['score']
            color = COLORS['success'] if score > 70 else COLORS['warning'] if score > 40 else COLORS['danger']
            
            opp_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.Span(opportunity['icon'], style={'fontSize': '2rem'}),
                                html.H6(opportunity['name'], style={'marginTop': '10px'}),
                                html.H3(str(score), style={'color': color, 'fontWeight': 'bold'}),
                                html.Small("Opportunity Score", className="text-muted")
                            ], style={'textAlign': 'center'})
                        ])
                    ], style={'backgroundColor': COLORS['card_bg'], 'border': f'2px solid {color}'})
                ], md=3)
            )
        
        sections.append(html.Div([
            html.H5("🎯 Opportunity Scores", 
                   style={'color': COLORS['primary'], 'marginTop': '20px', 'marginBottom': '15px'}),
            dbc.Row(opp_cards, className="mb-4")
        ]))
    
    # Anomaly Detection
    if insights.get('anomaly_detection'):
        anomaly = insights['anomaly_detection']
        
        if anomaly.get('status') == 'clean':
            sections.append(html.Div([
                html.H5("🔍 Anomaly Detection", 
                       style={'color': COLORS['primary'], 'marginTop': '20px', 'marginBottom': '15px'}),
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H3("✅", style={'fontSize': '3rem'}),
                            html.H5("No Anomalies Detected", style={'color': COLORS['success']}),
                            html.P("All systems operating normally", className="text-muted")
                        ], style={'textAlign': 'center', 'padding': '20px'})
                    ])
                ], style={'backgroundColor': COLORS['card_bg'], 'border': f'2px solid {COLORS["success"]}', 'marginBottom': '20px'})
            ]))
        elif anomaly.get('anomalies'):
            anomaly_items = []
            for anom in anomaly['anomalies']:
                severity_color = COLORS['danger'] if anom['severity'] == 'high' else COLORS['warning']
                anomaly_items.append(
                    dbc.ListGroupItem([
                        html.Div([
                            html.Span(f"⚠️ {anom['type'].replace('_', ' ').title()}", 
                                     style={'fontWeight': 'bold', 'color': severity_color}),
                            html.P(anom['description'], className="mb-1 mt-2"),
                            html.Small(f"Recommendation: {anom['recommendation']}", className="text-muted")
                        ])
                    ], style={'backgroundColor': COLORS['card_bg'], 'border': f'1px solid {severity_color}'})
                )
            
            sections.append(html.Div([
                html.H5("🔍 Anomaly Detection", 
                       style={'color': COLORS['primary'], 'marginTop': '20px', 'marginBottom': '15px'}),
                dbc.ListGroup(anomaly_items, className="mb-4")
            ]))
    
    return html.Div(sections) if sections else html.Div([
        html.P("AI insights will appear here after sufficient data is collected", 
               className="text-center text-muted",
               style={'padding': '40px'})
    ])


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

