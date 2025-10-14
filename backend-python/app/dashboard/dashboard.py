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
    
    # Auto-refresh interval
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # 30 seconds
        n_intervals=0
    ),
    
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
    
    # Footer
    html.Hr(style={'borderColor': COLORS['grid'], 'marginTop': '40px'}),
    html.P("PAIME - PlayMetric AI Metrics Engine v1.0 | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           style={'textAlign': 'center', 'color': COLORS['text'], 'opacity': '0.6', 'padding': '20px'})
    
], fluid=True, style={'backgroundColor': COLORS['background'], 'minHeight': '100vh', 'padding': '20px'})


# Callbacks
@callback(
    Output('key-metrics-row', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_key_metrics(n):
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
    Input('interval-component', 'n_intervals')
)
def update_user_activity(n):
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
    Input('interval-component', 'n_intervals')
)
def update_platform_distribution(n):
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
    Input('interval-component', 'n_intervals')
)
def update_level_difficulty(n):
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
    Input('interval-component', 'n_intervals')
)
def update_level_funnel(n):
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
    Input('interval-component', 'n_intervals')
)
def update_dropoff_levels(n):
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
    Input('interval-component', 'n_intervals')
)
def update_churn_risk(n):
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
    Input('interval-component', 'n_intervals')
)
def update_high_risk_users(n):
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
    Input('interval-component', 'n_intervals')
)
def update_recommendations(n):
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


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
