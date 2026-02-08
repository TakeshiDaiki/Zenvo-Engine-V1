import pandas as pd


# No-spell-check: ZENVO

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates indicators for the aggressive strategy."""
    # 1. EMA 50 (Immediate Trend)
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()

    # 2. RSI (Momentum)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    return df


def get_signal(df: pd.DataFrame) -> str:
    """Aggressive logic: Buy when RSI crosses 50 while price is above EMA 50."""
    if len(df) < 50:
        return 'NEUTRAL'

    current = df.iloc[-1]
    previous = df.iloc[-2]

    # BUY: Above EMA 50 and RSI crossing UP the 50 mark
    if current['close'] > current['ema50'] and previous['rsi'] < 50 <= current['rsi']:
        return 'BUY'

    # SELL: Below EMA 50 or RSI crossing DOWN the 50 mark
    if current['close'] < current['ema50'] or previous['rsi'] > 50 >= current['rsi']:
        return 'SELL'

    return 'NEUTRAL'