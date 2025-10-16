"""
PAIME Dashboard V3 - Real-time AI Analytics with Progressive Loading
All data from DB, no static content, with Excel export functionality
"""
import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, timezone
import requests
import pandas as pd
import numpy as np
from typing import Dict, List
from collections import defaultdict
import io
import base64

# Initialize Dash app with modern theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    title="PAIME - AI Game Analytics",
    suppress_callback_exceptions=True
)

# API Configuration
import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Enhanced Color Scheme
COLORS = {
    'background': '#0a0e27',
    'card_bg': '#1a1f3a',
    'card_border': '#2d3561',
    'text': '#e8eaf6',
    'text_secondary': '#9fa8da',
    'primary': '#00e5ff',
    'secondary': '#7c4dff',
    'success': '#00e676',
    'warning': '#ffd740',
    'danger': '#ff5252',
    'info': '#40c4ff',
    'purple': '#d500f9',
    'pink': '#f50057',
    'teal': '#1de9b6',
    'orange': '#ff9100',
    'grid': '#424242',
    'dropdown_bg': '#2d3561',
    'dropdown_text': '#ffffff'
}

# Vibrant gradient colors for charts
CHART_COLORS = [
    '#00e5ff', '#7c4dff', '#00e676', '#ffd740', '#ff5252',
    '#d500f9', '#f50057', '#1de9b6', '#ff9100', '#40c4ff'
]

# Dropdown Style (Fixed white text issue)
DROPDOWN_STYLE = {
    'backgroundColor': COLORS['dropdown_bg'],
    'color': COLORS['dropdown_text'],
    'border': f"1px solid {COLORS['card_border']}",
    'borderRadius': '6px'
}

def fetch_api_data(endpoint: str, timeout: int = 30) -> Dict:
    """Fetch data from API with extended timeout"""
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return {}

def create_metric_card(icon: str, title: str, value: str, subtitle: str = "", color: str = COLORS['primary'], trend: str = None):
    """Create an enhanced metric card with icon and trend"""
    trend_icon = ""
    trend_color = COLORS['success']
    if trend:
        if "↑" in trend or "+" in trend:
            trend_icon = "fa-arrow-trend-up"
            trend_color = COLORS['success']
        elif "↓" in trend or "-" in trend:
            trend_icon = "fa-arrow-trend-down"
            trend_color = COLORS['danger']
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas {icon} fa-2x", style={'color': color}),
            ], style={'marginBottom': '10px'}),
            html.H6(title, className="text-muted mb-2", style={'fontSize': '0.85rem'}),
            html.H3(value, style={'color': color, 'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.Div([
                html.P(subtitle, className="mb-0", style={'fontSize': '0.8rem', 'color': COLORS['text_secondary']}),
                html.P([
                    html.I(className=f"fas {trend_icon}", style={'marginRight': '5px'}),
                    trend
                ], style={'fontSize': '0.75rem', 'color': trend_color, 'marginTop': '5px'}) if trend else None
            ])
        ])
    ], style={
        'backgroundColor': COLORS['card_bg'],
        'border': f"1px solid {COLORS['card_border']}",
        'borderRadius': '12px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
        'height': '100%'
    })

def create_ai_insight_card(title: str, insights: List[str], severity: str = "info"):
    """Create AI insight card with severity indicator"""
    severity_colors = {
        'critical': COLORS['danger'],
        'warning': COLORS['warning'],
        'success': COLORS['success'],
        'info': COLORS['info']
    }
    severity_icons = {
        'critical': 'fa-triangle-exclamation',
        'warning': 'fa-circle-exclamation',
        'success': 'fa-circle-check',
        'info': 'fa-lightbulb'
    }
    
    color = severity_colors.get(severity, COLORS['info'])
    icon = severity_icons.get(severity, 'fa-lightbulb')
    
    return dbc.Alert([
        html.H5([
            html.I(className=f"fas {icon}", style={'marginRight': '10px'}),
            title
        ], style={'color': color, 'marginBottom': '10px'}),
        html.Ul([html.Li(insight, style={'marginBottom': '8px'}) for insight in insights])
    ], color="dark", style={'backgroundColor': COLORS['card_bg'], 'border': f'2px solid {color}'})

def create_loading_spinner(component_id: str):
    """Create a loading spinner for progressive loading"""
    return dcc.Loading(
        id=f"loading-{component_id}",
        type="default",
        color=COLORS['primary'],
        children=html.Div(id=component_id)
    )

# Layout
app.layout = dbc.Container([
    # Hidden div for refresh trigger
    html.Div(id='refresh-trigger', style={'display': 'none'}),
    
    # Hidden div for export data storage
    dcc.Store(id='export-data-store'),
    dcc.Download(id='download-excel'),
    
    # Header
    dbc.Row([
        dbc.Col([
            html.H1([
                html.I(className="fas fa-brain", style={'marginRight': '15px', 'color': COLORS['primary']}),
                "PAIME Dashboard V3"
            ], style={'color': COLORS['text'], 'marginBottom': '5px'}),
            html.P("AI-Powered Game Analytics - Real-time Insights", 
                   style={'color': COLORS['text_secondary'], 'fontSize': '1.1rem'})
        ], md=8),
        dbc.Col([
            html.Div([
                dbc.Button([
                    html.I(className="fas fa-sync-alt", style={'marginRight': '8px'}),
                    "Refresh Data"
                ], id='refresh-button', color="primary", size="lg", style={'marginBottom': '10px', 'width': '100%'}),
                dbc.Button([
                    html.I(className="fas fa-file-excel", style={'marginRight': '8px'}),
                    "Export Report"
                ], id='export-button', color="success", outline=True, size="lg", style={'width': '100%'}),
            ], style={'textAlign': 'right'})
        ], md=4),
    ], className="mb-4", style={'borderBottom': f'2px solid {COLORS["card_border"]}', 'paddingBottom': '20px'}),
    
    # Last Refresh Time
    html.P(id='last-refresh-time', style={'textAlign': 'right', 'color': COLORS['text_secondary'], 'fontSize': '0.9rem'}),
    
    # Tabs
    dbc.Tabs([
        dbc.Tab(label="📊 Overview", tab_id="overview", tab_style={'backgroundColor': COLORS['card_bg']}, 
                active_label_style={'backgroundColor': COLORS['primary'], 'color': '#000'}),
        dbc.Tab(label="👥 User Analytics", tab_id="users", tab_style={'backgroundColor': COLORS['card_bg']},
                active_label_style={'backgroundColor': COLORS['primary'], 'color': '#000'}),
        dbc.Tab(label="🎮 Game Analytics", tab_id="game", tab_style={'backgroundColor': COLORS['card_bg']},
                active_label_style={'backgroundColor': COLORS['primary'], 'color': '#000'}),
        dbc.Tab(label="🎯 Level Analytics", tab_id="levels", tab_style={'backgroundColor': COLORS['card_bg']},
                active_label_style={'backgroundColor': COLORS['primary'], 'color': '#000'}),
        dbc.Tab(label="💰 Monetization", tab_id="monetization", tab_style={'backgroundColor': COLORS['card_bg']},
                active_label_style={'backgroundColor': COLORS['primary'], 'color': '#000'}),
        dbc.Tab(label="🤖 AI Insights", tab_id="ai", tab_style={'backgroundColor': COLORS['card_bg']},
                active_label_style={'backgroundColor': COLORS['primary'], 'color': '#000'}),
    ], id="tabs", active_tab="overview", style={'marginBottom': '20px'}),
    
    # Tab Content with Progressive Loading
    create_loading_spinner('tab-content'),
    
    # Footer
    html.Hr(style={'borderColor': COLORS['grid'], 'marginTop': '40px'}),
    html.P([
        html.I(className="fas fa-brain", style={'marginRight': '10px', 'color': COLORS['primary']}),
        "PAIME v3.0 - Real-time AI Analytics | Last updated: ",
        html.Span(id='footer-timestamp')
    ], style={'textAlign': 'center', 'color': COLORS['text_secondary'], 'padding': '20px'})
    
], fluid=True, style={
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'padding': '20px'
})

# Callback: Refresh Trigger
@callback(
    Output('refresh-trigger', 'children'),
    Output('last-refresh-time', 'children'),
    Output('footer-timestamp', 'children'),
    Input('refresh-button', 'n_clicks'),
    prevent_initial_call=False
)
def trigger_refresh(n_clicks):
    """Trigger data refresh"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(n_clicks or 0), f"Last refreshed: {now}", now

# Callback: Tab Content Dispatcher
@callback(
    Output('tab-content', 'children'),
    Input('tabs', 'active_tab'),
    Input('refresh-trigger', 'children')
)
def render_tab_content(active_tab, trigger):
    """Route to appropriate tab renderer"""
    if active_tab == "overview":
        return render_overview()
    elif active_tab == "users":
        return render_user_analytics()
    elif active_tab == "game":
        return render_game_analytics()
    elif active_tab == "levels":
        return render_level_analytics()
    elif active_tab == "monetization":
        return render_monetization()
    elif active_tab == "ai":
        return render_ai_insights()
    return html.Div("Select a tab", className="text-center", style={'padding': '50px'})

def render_overview():
    """Overview tab layout"""
    return html.Div([
        # KPIs will be loaded dynamically
        html.Div(id='overview-kpis'),
        html.Hr(style={'borderColor': COLORS['grid'], 'margin': '30px 0'}),
        # Charts will be loaded dynamically
        html.Div(id='overview-charts')
    ])

def render_user_analytics():
    """User analytics tab layout"""
    return html.Div([
        # Filters
        dbc.Card([
            dbc.CardHeader("🔍 User Filters", style={'backgroundColor': COLORS['card_bg'], 'color': COLORS['text']}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("User Segment:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='user-segment-filter',
                            options=[
                                {'label': '🐋 Whales (High Spenders)', 'value': 'whales'},
                                {'label': '⚡ Engaged Players', 'value': 'engaged'},
                                {'label': '😊 Casual Players', 'value': 'casual'},
                                {'label': '⚠️ At Risk', 'value': 'at_risk'},
                                {'label': '🆕 New Users', 'value': 'new'},
                                {'label': '😴 Dormant', 'value': 'dormant'},
                                {'label': '🌐 All Users', 'value': 'all'}
                            ],
                            value='all',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=3),
                    dbc.Col([
                        html.Label("Platform:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='user-platform-filter',
                            options=[
                                {'label': '🤖 Android', 'value': 'Android'},
                                {'label': '🍎 iOS', 'value': 'iOS'},
                                {'label': '🌐 Web', 'value': 'Web'},
                                {'label': '🌍 All Platforms', 'value': 'all'}
                            ],
                            value='all',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=3),
                    dbc.Col([
                        html.Label("Date Range:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='user-date-filter',
                            options=[
                                {'label': '📅 Last 7 Days', 'value': '7'},
                                {'label': '📅 Last 14 Days', 'value': '14'},
                                {'label': '📅 Last 30 Days', 'value': '30'},
                                {'label': '📅 All Time', 'value': 'all'}
                            ],
                            value='30',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=3),
                    dbc.Col([
                        html.Label("Churn Risk:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='user-churn-filter',
                            options=[
                                {'label': '🔴 Critical Risk', 'value': 'critical'},
                                {'label': '🟠 High Risk', 'value': 'high'},
                                {'label': '🟡 Medium Risk', 'value': 'medium'},
                                {'label': '🟢 Low Risk', 'value': 'low'},
                                {'label': '🌐 All Levels', 'value': 'all'}
                            ],
                            value='all',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=3),
                ])
            ])
        ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none', 'marginBottom': '20px'}),
        
        # Content will be loaded dynamically
        html.Div(id='user-analytics-content')
    ])

def render_game_analytics():
    """Game analytics tab layout"""
    return html.Div([
        # Filters
        dbc.Card([
            dbc.CardHeader("🔍 Game Filters", style={'backgroundColor': COLORS['card_bg'], 'color': COLORS['text']}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Session Type:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='game-session-filter',
                            options=[
                                {'label': '⚡ Short (< 5 min)', 'value': 'short'},
                                {'label': '⏱️ Medium (5-15 min)', 'value': 'medium'},
                                {'label': '⏰ Long (> 15 min)', 'value': 'long'},
                                {'label': '🌐 All Sessions', 'value': 'all'}
                            ],
                            value='all',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Game Mode:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='game-mode-filter',
                            options=[
                                {'label': '🗺️ Campaign', 'value': 'campaign'},
                                {'label': '⚔️ PvP', 'value': 'pvp'},
                                {'label': '♾️ Endless', 'value': 'endless'},
                                {'label': '🌐 All Modes', 'value': 'all'}
                            ],
                            value='all',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Performance Metric:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='game-metric-filter',
                            options=[
                                {'label': '📊 Difficulty', 'value': 'difficulty'},
                                {'label': '⏱️ Time', 'value': 'time'},
                                {'label': '🎯 Success Rate', 'value': 'success'},
                                {'label': '💰 Revenue', 'value': 'revenue'}
                            ],
                            value='difficulty',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=4),
                ])
            ])
        ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none', 'marginBottom': '20px'}),
        
        # Content will be loaded dynamically
        html.Div(id='game-analytics-content')
    ])

def render_level_analytics():
    """Level analytics tab layout"""
    return html.Div([
        # Filters
        dbc.Card([
            dbc.CardHeader("🔍 Level Filters", style={'backgroundColor': COLORS['card_bg'], 'color': COLORS['text']}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Level Range:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.RangeSlider(
                            id='level-range-filter',
                            min=1,
                            max=50,
                            step=1,
                            value=[1, 50],
                            marks={i: str(i) for i in range(1, 51, 5)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], md=6),
                    dbc.Col([
                        html.Label("Difficulty:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='level-difficulty-filter',
                            options=[
                                {'label': '😊 Easy', 'value': 'easy'},
                                {'label': '⚠️ Medium', 'value': 'medium'},
                                {'label': '🔥 Hard', 'value': 'hard'},
                                {'label': '🌐 All', 'value': 'all'}
                            ],
                            value='all',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=3),
                    dbc.Col([
                        html.Label("Sort By:", style={'color': COLORS['text'], 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='level-sort-filter',
                            options=[
                                {'label': '📈 Completion Rate', 'value': 'completion'},
                                {'label': '⏱️ Duration', 'value': 'duration'},
                                {'label': '💀 Deaths', 'value': 'deaths'}
                            ],
                            value='completion',
                            style=DROPDOWN_STYLE,
                            className='dark-dropdown'
                        )
                    ], md=3),
                ])
            ])
        ], style={'backgroundColor': COLORS['card_bg'], 'border': 'none', 'marginBottom': '20px'}),
        
        # Content will be loaded dynamically
        html.Div(id='level-analytics-content')
    ])

def render_monetization():
    """Monetization tab layout"""
    return html.Div([
        html.Div(id='monetization-content')
    ])

def render_ai_insights():
    """AI Insights tab layout"""
    return html.Div([
        html.Div(id='ai-insights-content')
    ])

# Add CSS for dropdown styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .dark-dropdown .Select-control {
                background-color: #2d3561 !important;
                color: #ffffff !important;
            }
            .dark-dropdown .Select-menu-outer {
                background-color: #2d3561 !important;
                color: #ffffff !important;
            }
            .dark-dropdown .Select-option {
                background-color: #2d3561 !important;
                color: #ffffff !important;
            }
            .dark-dropdown .Select-option:hover {
                background-color: #3d4571 !important;
                color: #ffffff !important;
            }
            .dark-dropdown .Select-value-label {
                color: #ffffff !important;
            }
            .dark-dropdown .Select-placeholder {
                color: #9fa8da !important;
            }
            /* New dropdown styling for dcc.Dropdown */
            .dash-dropdown .Select-control,
            .dash-dropdown .Select-menu-outer,
            .dash-dropdown .Select-menu,
            .dash-dropdown .VirtualizedSelectOption {
                background-color: #2d3561 !important;
                color: #ffffff !important;
            }
            .dash-dropdown .Select-value-label,
            .dash-dropdown .Select-input > input {
                color: #ffffff !important;
            }
            .dash-dropdown .Select-option {
                color: #ffffff !important;
                background-color: #2d3561 !important;
            }
            .dash-dropdown .Select-option:hover {
                background-color: #3d4571 !important;
            }
            .dash-dropdown .Select-option.is-selected {
                background-color: #00e5ff !important;
                color: #000000 !important;
            }
            /* Fix for modern dash dropdown */
            .dash-dropdown div[class*="menu"] {
                background-color: #2d3561 !important;
            }
            .dash-dropdown div[class*="option"] {
                color: #ffffff !important;
                background-color: #2d3561 !important;
            }
            .dash-dropdown div[class*="option"]:hover {
                background-color: #3d4571 !important;
            }
            .dash-dropdown div[class*="singleValue"],
            .dash-dropdown div[class*="placeholder"] {
                color: #ffffff !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Now I'll continue with the callback implementations in the next file...
# This file is getting too long, so I'll create a separate callbacks file
