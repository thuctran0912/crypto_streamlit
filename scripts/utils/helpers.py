import time
import pytz
from datetime import datetime

def get_unique_key(base_key: str) -> str:
    """Generate a unique key based on timestamp"""
    return f"{base_key}_{int(time.time())}"

def convert_to_local_time(utc_time):
    """Convert UTC timestamp to Helsinki time (UTC+3)"""
    if utc_time is None:
        return None
        
    helsinki_tz = pytz.timezone('Europe/Helsinki')
    
    # If the timestamp is naive (no timezone info), assume it's UTC
    if utc_time.tzinfo is None:
        utc_time = pytz.utc.localize(utc_time)
    
    return utc_time.astimezone(helsinki_tz)

def format_price_change(current_price, previous_price):
    """Format price change with color and arrow"""
    if previous_price is None:
        return "", "gray"
    
    change = current_price - previous_price
    color = "green" if change >= 0 else "red"
    arrow = "↑" if change >= 0 else "↓"
    return f"{arrow} ({abs(change):.2f})", color
