import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Credentials (read from the .env file)
API_KEY = os.getenv('BINANCE_API_KEY') or ""
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY') or ""

# Market Parameters
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'

# Strategy Parameters
EMA_FAST = 50
EMA_SLOW = 200
RSI_PERIOD = 14
VOL_PERIOD = 20

# Risk Management
QUANTITY = 0.001    # BTC amount to trade
TP_PERCENT = 0.015  # 1.5% Take Profit
SL_PERCENT = 0.0075 # 0.75% Stop Loss (1:2 Risk/Reward Ratio)