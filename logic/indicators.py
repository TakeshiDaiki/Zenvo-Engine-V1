# No-spell-check: ZENVO

def add_indicators(df):
    try:
        # EMAs
        df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
        df['ema200'] = df['close'].ewm(span=200, adjust=False).mean()

        # RSI 14 (Wilder's Smoothing)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0))
        loss = (-delta.where(delta < 0, 0))
        avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()

        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # Volume Average
        df['vol_avg'] = df['volume'].rolling(window=20).mean()

        return df
    except Exception as e:
        print(f"Indicator Error: {e}")
        return df