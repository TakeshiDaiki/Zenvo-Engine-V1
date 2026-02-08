import ccxt
import pandas as pd


class BinanceClient:
    """
    Handles Binance API interactions with automatic LOT_SIZE normalization.
    Standardized for Testnet and Real accounts.
    """

    def __init__(self, api_key="", secret_key="", mode="testnet"):
        # adjustForTimeDifference prevents the common 'Timestamp for this request' error
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True
            }
        })

        # Standardize mode check
        if mode == "testnet":
            self.exchange.set_sandbox_mode(True)
            print("🌐 [SYSTEM] Connected to Binance TESTNET (Demo Mode)")
        else:
            print("💰 [SYSTEM] Connected to Binance REAL ACCOUNT")

    def create_order(self, symbol, side, amount_usd):
        """
        Executes a market order by converting USD amount to crypto quantity.
        Uses exchange precision rules to avoid LOT_SIZE errors.
        """
        try:
            self.exchange.load_markets()
            ticker = self.exchange.fetch_ticker(symbol)
            current_price = ticker['last']

            if side == 'buy':
                raw_amount = float(amount_usd) / current_price
            else:
                raw_amount = float(amount_usd)

            # Normalizes amount according to Binance precision rules
            precise_amount = self.exchange.amount_to_precision(symbol, raw_amount)

            self.exchange.create_order(symbol, 'market', side, precise_amount)
            return True

        except (ccxt.NetworkError, ccxt.ExchangeError) as e:
            print(f"\n❌ Order Error: {e}")
            return False

    def get_balance(self, asset="USDT"):
        """Fetches the free balance of a specific asset."""
        try:
            bal = self.exchange.fetch_balance()
            return float(bal.get(asset, {}).get('free', 0))
        except Exception as e:
            raise e

    def get_klines(self, symbol, timeframe):
        """Fetches OHLCV data and returns a formatted DataFrame."""
        bars = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df