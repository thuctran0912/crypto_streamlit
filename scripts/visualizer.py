import plotly.graph_objects as go
import pytz
from datetime import datetime

def convert_to_local_time(utc_time):
    """
    Convert UTC timestamp to Helsinki time (UTC+3)
    
    Parameters:
    - utc_time: datetime object in UTC
    
    Returns:
    - datetime object in Helsinki time
    """
    if utc_time is None:
        return None
        
    helsinki_tz = pytz.timezone('Europe/Helsinki')
    
    # If the timestamp is naive (no timezone info), assume it's UTC
    if utc_time.tzinfo is None:
        utc_time = pytz.utc.localize(utc_time)
    
    return utc_time.astimezone(helsinki_tz)

def create_price_chart(historical_data, crypto):
    """
    Create an interactive price chart using Plotly
    
    Parameters:
    - historical_data: DataFrame containing the price data with local time
    - crypto: String indicating the cryptocurrency (e.g., 'BTC', 'ETH')
    """
    if len(historical_data) > 0:
        fig = go.Figure()
        
        # Set different colors for BTC and ETH
        colors = {
            'BTC': '#FF9500',  # Orange for Bitcoin
            'ETH': '#627EEA'   # Blue for Ethereum
        }
        
        fig.add_trace(go.Scatter(
            x=historical_data['TRADE_TIME'],
            y=historical_data['AVG_PRICE'],
            mode='lines+markers',
            name=f'{crypto} Price',
            line=dict(
                color=colors.get(crypto, '#2962FF'),
                width=2
            ),
            marker=dict(
                size=6
            )
        ))
        
        fig.update_layout(
            title=dict(
                text=f'Price Movement (Last 30 Seconds)',
                x=0.5,
                xanchor='center'
            ),
            xaxis_title='Time (Helsinki)',
            yaxis_title='Price (USDT)',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(128,128,128,0.1)',
                tickformat='%H:%M:%S'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(128,128,128,0.1)',
                tickprefix='$'
            ),
            hovermode='x unified'
        )
        
        # Add hover template to show local time
        fig.update_traces(
            hovertemplate=(
                "Time: %{x|%H:%M:%S}<br>" +
                "Price: $%{y:,.2f}<br>" +
                "<extra></extra>"
            )
        )
        
        return fig
    return None

def format_price_change(current_price, previous_price):
    """Format price change with color and arrow"""
    if previous_price is None:
        return "", "gray"
    
    change = current_price - previous_price
    color = "green" if change >= 0 else "red"
    arrow = "↑" if change >= 0 else "↓"
    return f"{arrow} ({abs(change):.2f})", color

def get_custom_css():
    """Return custom CSS styles for the dashboard"""
    return """
    <style>
    .stApp {
        max-width: 100%;
    }
    .crypto-metric {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .element-container iframe {
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        background-color: white;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
    </style>
    """
