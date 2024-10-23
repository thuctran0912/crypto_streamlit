import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col, current_timestamp, max
from decimal import Decimal


def get_combined_crypto_data(session, crypto):
    """
    Fetches historical and latest crypto price data from Snowflake using Snowpark.
    
    Parameters:
    - session: The active Snowpark session.
    - crypto: The cryptocurrency symbol (e.g., 'BTC', 'ETH').

    Returns:
    - historical_data: DataFrame containing historical price data.
    - latest_price: The latest price of the cryptocurrency.
    - latest_trade_time: The timestamp of the latest trade.
    """
    try:
        # Load the view using Snowpark
        trading_view = session.table(f"MSK_STREAMING_DB.MSK_STREAMING_SCHEMA.{crypto}_TRADING_VIEW")

        # First get the latest timestamp
        latest_timestamp = trading_view.select(max(col("TRADE_TIME"))).collect()[0][0]
        
        # Fetch historical data for the last 30 seconds from the latest timestamp
        historical_data = (
            trading_view
            .filter(col("TRADE_TIME") >= latest_timestamp - pd.Timedelta(seconds=30))
            .sort(col("TRADE_TIME").asc())
            .to_pandas()
        )

        # Get the latest price (we can use the latest timestamp we already found)
        latest_data = (
            trading_view
            .filter(col("TRADE_TIME") == latest_timestamp)
            .collect()
        )

        if latest_data:
            latest_price = latest_data[0]["AVG_PRICE"]
            latest_trade_time = pd.to_datetime(latest_data[0]["TRADE_TIME"])
            return historical_data, latest_price, latest_trade_time
        else:
            return historical_data, None, None
    except Exception as e:
        st.error(f"Error fetching {crypto} data: {str(e)}")
        return pd.DataFrame(), None, None

  
def get_crypto_news(session):
    """
    Fetches the latest cryptocurrency-related news using Snowpark.
    
    Args:
        session: Active Snowpark session
    
    Returns:
        pandas.DataFrame: DataFrame containing news data with columns:
            - SOURCE: News source
            - HEADLINE: News headline
            - URL: Link to full article
    """
    try:
        # Create Snowpark DataFrame
        news_table = session.table('BATCH_DB.HISTORY_FINNHUB.FINNHUB_NEWS')
        
        # Query using Snowpark operations
        news_data = (
            news_table
            .select(['SOURCE', 'HEADLINE', 'URL'])
            .sort(col('DATETIME').desc())
            .limit(10)
            .to_pandas()
        )
        
        return news_data
    except Exception as e:
        st.error(f"Error fetching news data: {str(e)}")
        return pd.DataFrame()


def get_portfolio(session):
    """
    Fetches portfolio data using Snowpark.
    
    Args:
        session: Active Snowpark session
        
    Returns:
        pandas.DataFrame: Portfolio data
    """
    try:
        portfolio_table = session.table('VISUALIZATION_DB.PORTIFOLIO.PORTFOLIO')
        portfolio_data = (
            portfolio_table
            .select(['SYMBOL', 'PRICE_PER_UNIT_BOUGHT', 'QUANTITY'])
            .to_pandas()
        )
        return portfolio_data
    except Exception as e:
        st.error(f"Error fetching portfolio data: {str(e)}")
        return pd.DataFrame()


def calculate_portfolio_performance(portfolio_df, current_prices):
    """
    Calculate portfolio performance metrics.
    
    Args:
        portfolio_df: DataFrame with portfolio data
        current_prices: Dict mapping symbols to current prices
        
    Returns:
        tuple: (updated_portfolio, total_pl, total_value, percent_change)
    """
    try:
        if len(portfolio_df) == 0:
            return pd.DataFrame(), 0.0, 0.0, 0.0

        # Create a copy to avoid modifying the original
        portfolio = portfolio_df.copy()

        def to_decimal(value):
            if isinstance(value, Decimal):
                return value
            return Decimal(str(value)) if value is not None else Decimal('0')

        # Convert to Decimal for precision
        portfolio['QUANTITY'] = portfolio['QUANTITY'].apply(to_decimal)
        portfolio['PRICE_PER_UNIT_BOUGHT'] = portfolio['PRICE_PER_UNIT_BOUGHT'].apply(to_decimal)
        portfolio['current_price'] = portfolio['SYMBOL'].map(current_prices).apply(to_decimal)

        # Calculate metrics
        portfolio['current_value'] = portfolio['QUANTITY'] * portfolio['current_price']
        portfolio['bought_value'] = portfolio['QUANTITY'] * portfolio['PRICE_PER_UNIT_BOUGHT']
        portfolio['profit_loss'] = portfolio['current_value'] - portfolio['bought_value']
        portfolio['percent_change'] = ((portfolio['current_price'] - portfolio['PRICE_PER_UNIT_BOUGHT']) 
                                     / portfolio['PRICE_PER_UNIT_BOUGHT'] * 100)

        # Calculate totals
        total_pl = float(portfolio['profit_loss'].sum())
        total_value = float(portfolio['current_value'].sum())
        total_bought = float(portfolio['bought_value'].sum())
        overall_change = float(((total_value - total_bought) / total_bought * 100) if total_bought != 0 else 0)

        return portfolio, total_pl, total_value, overall_change
    except Exception as e:
        st.error(f"Error calculating portfolio performance: {str(e)}")
        return pd.DataFrame(), 0.0, 0.0, 0.0