import websocket
import os
from dotenv import load_dotenv

# Load environment variables from config.env
load_dotenv('config.env')

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:ETHUSDT"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    
    # Get the API key from environment variables
    api_key = os.getenv('FINNHUB_API_KEY')
    
    if not api_key:
        raise ValueError("FINNHUB_API_KEY not found in environment variables")
    
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={api_key}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
