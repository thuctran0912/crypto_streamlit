import streamlit as st
import plotly.express as px
from ..utils.helpers import get_unique_key, convert_to_local_time, format_price_change
from ..utils.constants import CHART_LAYOUT, VOLUME_CHART_LAYOUT

class CryptoCard:
    def __init__(self, symbol: str, color: str):
        self.symbol = symbol
        self.color = color
        self.name = 'Bitcoin' if symbol == 'BTC' else 'Ethereum'
    
    def create_price_chart(self, data):
        """Create the price movement chart"""
        fig = px.line(
            data,
            x='TRADE_TIME',
            y='AVG_PRICE',
            title='Price Movement (Last 30 Seconds)',
            labels={'TRADE_TIME': 'Time', 'AVG_PRICE': 'Price (USDT)'}
        )
        
        fig.update_traces(
            line_color=self.color,
            line_width=2,
            mode='lines+markers'
        )
        
        fig.update_layout(**CHART_LAYOUT)
        return fig
    
    def create_volume_chart(self, data):
        """Create the volume analysis chart"""
        if 'VOLUME' in data.columns:
            fig = px.bar(
                data,
                x='TRADE_TIME',
                y='VOLUME',
                title='Trading Volume',
                labels={'TRADE_TIME': 'Time', 'VOLUME': 'Volume'},
                color_discrete_sequence=[self.color]
            )
            
            fig.update_layout(**VOLUME_CHART_LAYOUT)
            return fig
        return None
    
    def display(self, data, price, timestamp, previous_price):
        """Display the complete crypto card"""
        st.subheader(f"{self.name} ({self.symbol})")
        
        if price is not None:
            # Price metric
            price_change, _ = format_price_change(price, previous_price)
            st.metric(
                label=f"{self.symbol}/USDT",
                value=f"${price:,.2f}",
                delta=price_change
            )
            
            # Timestamp
            local_time = convert_to_local_time(timestamp)
            st.caption(f"Last updated: {local_time.strftime('%Y-%m-%d %H:%M:%S')} (Helsinki)")
            
            if len(data) > 0:
                # Convert timestamps
                data = data.copy()
                data['TRADE_TIME'] = data['TRADE_TIME'].apply(convert_to_local_time)
                
                # Price chart
                price_fig = self.create_price_chart(data)
                st.plotly_chart(
                    price_fig, 
                    use_container_width=True, 
                    key=get_unique_key(f'{self.symbol.lower()}_price')
                )
                
                # Volume chart
                volume_fig = self.create_volume_chart(data)
                if volume_fig:
                    st.plotly_chart(
                        volume_fig, 
                        use_container_width=True, 
                        key=get_unique_key(f'{self.symbol.lower()}_volume')
                    )
        else:
            st.write(f"No {self.symbol} data available")
