# No-spell-check: ZENVO

def add_indicators(df):
    """
    Calculates technical indicators for the Zenvo Bot.
    Includes EMA 9 (Safety Filter), EMA 50, EMA 200, and RSI 14.
    """
    try:
        # --- MOVING AVERAGES ---
        # EMA 9 is your primary safety filter for confirmed entries
        df['ema9'] = df['close'].ewm(span=9, adjust=False).mean()

        # Long-term trend indicators
        df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
        df['ema200'] = df['close'].ewm(span=200, adjust=False).mean()

        # --- RSI 14 (Wilder's Smoothing) ---
        # We use Wilder's method for smoother and more reliable signals
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0))
        loss = (-delta.where(delta < 0, 0))

        # alpha=1/14 is the standard for Wilder's RSI
        avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()

        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # --- VOLUME ---
        # Calculating 20-period volume average for liquidity context
        df['vol_avg'] = df['volume'].rolling(window=20).mean()

        return df

    except Exception as e:
        print(f"❌ Indicator Calculation Error: {e}")
        return df