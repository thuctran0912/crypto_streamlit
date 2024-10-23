import streamlit as st
import time
from scripts.components.crypto_card import CryptoCard
from scripts.components.news_card import NewsCard
from scripts.components.portfolio_card import PortfolioCard
from scripts.utils.constants import COLOR_MAP
from scripts.fetcher import (
    get_combined_crypto_data, 
    get_crypto_news,
    get_portfolio,
    calculate_portfolio_performance
)

def initialize_session_state():
    """Initialize session state variables"""
    for crypto in ['BTC', 'ETH']:
        if f'previous_price_{crypto}' not in st.session_state:
            st.session_state[f'previous_price_{crypto}'] = None

def initialize_page():
    """Configure initial page settings"""
    st.set_page_config(
        page_title="Crypto Trading Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Add custom CSS for better spacing and layout
    st.markdown("""
        <style>
        .main {
            padding-top: 1rem;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    # Initialize page configuration
    initialize_page()
    
    # Initialize session state
    initialize_session_state()
    
    # Page title and description
    st.title("📈 Crypto Trading Dashboard")
    st.caption("Real-time cryptocurrency prices, news, and portfolio tracking | All times shown in Helsinki time (UTC+3)")
    
    # Initialize Snowflake connection
    conn = st.connection("snowflake")
    session = conn.session()
    
    # Initialize components
    btc_card = CryptoCard('BTC', COLOR_MAP['BTC'])
    eth_card = CryptoCard('ETH', COLOR_MAP['ETH'])
    news_card = NewsCard()
    portfolio_card = PortfolioCard()
    
    # Create a placeholder for the entire dashboard
    placeholder = st.empty()
    
    # Main dashboard loop
    while True:
        with placeholder.container():
            try:
                # First row: Crypto prices and news
                price_news_cols = st.columns([2, 2, 1])
                
                # BTC Column
                with price_news_cols[0]:
                    btc_data, btc_price, btc_time = get_combined_crypto_data(session, 'BTC')
                    btc_card.display(
                        btc_data,
                        btc_price,
                        btc_time,
                        st.session_state.previous_price_BTC
                    )
                    st.session_state.previous_price_BTC = btc_price if btc_price is not None else st.session_state.previous_price_BTC
                
                # ETH Column
                with price_news_cols[1]:
                    eth_data, eth_price, eth_time = get_combined_crypto_data(session, 'ETH')
                    eth_card.display(
                        eth_data,
                        eth_price,
                        eth_time,
                        st.session_state.previous_price_ETH
                    )
                    st.session_state.previous_price_ETH = eth_price if eth_price is not None else st.session_state.previous_price_ETH
                
                # News Column
                with price_news_cols[2]:
                    news_data = get_crypto_news(session)
                    news_card.display(news_data)
                
                # Add separator between sections
                st.markdown("---")
                
                # Second row: Portfolio section
                portfolio_data = get_portfolio(session)
                
                # Create current prices dictionary
                current_prices = {
                    'BTC': btc_price if btc_price is not None else 0,
                    'ETH': eth_price if eth_price is not None else 0
                }
                
                # Calculate portfolio performance
                updated_portfolio, total_pl, total_value, overall_change = calculate_portfolio_performance(
                    portfolio_data,
                    current_prices
                )
                
                # Display portfolio information
                portfolio_card.display(
                    updated_portfolio,
                    total_pl,
                    total_value,
                    overall_change
                )
                
            except Exception as e:
                st.error(f"An error occurred while updating the dashboard: {str(e)}")
                # Log error here if needed
            
            # Wait before next update
            time.sleep(1)

if __name__ == "__main__":
    main()
