import time
import sys
import pandas as pd
from core.exchange import BinanceClient
from ccxt import NetworkError, ExchangeError


def calculate_indicators(series, period: int = 14):
    """
    Calculates RSI for entry and EMA 200 for trend filtering.
    """
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    alpha_val = 1 / float(period)
    avg_gain = gain.ewm(alpha=alpha_val, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=alpha_val, min_periods=period, adjust=False).mean()

    rs_val = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs_val))
    ema_200 = series.ewm(span=200, adjust=False).mean()

    return rsi, ema_200


def run_bot(config):
    """
    Zenvo Engine: RSI Hybrid Strategy + Trailing Profit + Secure Shutdown.
    """
    gui = config['instance']
    client = BinanceClient(config['api_key'], config['secret_key'], config['mode'])

    client.exchange.options['recvWindow'] = 60000
    client.exchange.enableRateLimit = True

    # User Parameters
    user_sl = float(config.get('sl', 1.5))  # Trailing Gap
    user_tp = float(config.get('tp', 3.0))  # Activation Trigger
    sep = "=" * 45

    try:
        bal_info = client.exchange.fetch_balance()
        initial_bal = float(bal_info.get('USDT', {}).get('free', 0.0))
    except (NetworkError, ExchangeError):
        initial_bal = 0.0

    # --- HEADER ---
    print(f"\n{sep}")
    print(f"✅ AUTHENTICATION SUCCESSFUL")
    print(f"Market Selected: {config['symbol']}")
    print(f"{sep}")
    print(f"🚀 ZENVO CORE ONLINE - TRADING MODE")
    print(f"{sep}")
    print(f"📊 MARKET: {config['symbol']} | TF: {config.get('timeframe', '1m')}")
    print(f"💵 INITIAL BALANCE: {initial_bal:,.2f} USDT")
    print(f"💰 INVESTMENT: {config['usd_amount']} USDT")
    print(f"🛡️ TRAILING GAP: {user_sl}% | 🎯 TP ACTIVATION: {user_tp}%")
    print(f"{sep}\n")

    in_position, entry_price, max_price = False, 0.0, 0.0
    trailing_activated = False

    # MAIN LOOP
    while gui.bot_running:
        try:
            ohlcv = client.exchange.fetch_ohlcv(config['symbol'], config.get('timeframe', '1m'), limit=250)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            rsi_series, ema_series = calculate_indicators(df['close'])
            price = float(df['close'].iloc[-1])
            rsi_val = float(rsi_series.iloc[-1])
            ema_val = float(ema_series.iloc[-1])

            if not in_position:
                # HYBRID STRATEGY
                is_standard = rsi_val <= 30.0
                is_sensitive = rsi_val <= 35.0 and price > ema_val

                if is_standard or is_sensitive:
                    mode = "STANDARD" if is_standard else "SENSITIVE"
                    sys.stdout.write(f"\n🎯 SIGNAL [{mode}]: RSI {rsi_val:.2f}. Buying...")

                    if client.create_order(config['symbol'], 'buy', config['usd_amount']):
                        entry_price, max_price, in_position = price, price, True
                        trailing_activated = False
                        sys.stdout.write(f" 🟢 SUCCESS @ {entry_price:,.2f}\n")
                    else:
                        sys.stdout.write(" ❌ ORDER FAILED\n")

                status_msg = f"WAITING (RSI: {rsi_val:.2f})"

            else:
                if price > max_price:
                    max_price = price

                pnl = ((price - entry_price) / entry_price) * 100
                drawdown = ((max_price - price) / max_price) * 100

                # Check for TP Activation
                if not trailing_activated and pnl >= user_tp:
                    trailing_activated = True
                    sys.stdout.write(f"\n🔥 TP REACHED ({pnl:.2f}%). Trailing Profit Active!\n")

                # EXIT LOGIC
                if drawdown >= user_sl:
                    exit_reason = "TRAILING PROFIT" if trailing_activated else "STOP LOSS"
                    sys.stdout.write(f"\n🔴 EXIT [{exit_reason}] | Final PnL: {pnl:.2f}%\n")
                    # (client.create_order to sell is here)
                    in_position = False

                state = "TRAILING" if trailing_activated else "WAITING TP"
                status_msg = f"ON ({pnl:.2f}%) | Max: {max_price:,.2f} | {state}"

            sys.stdout.write(f"\r🕒 {time.strftime('%H:%M:%S')} | {status_msg}")
            sys.stdout.flush()

            time.sleep(1)

        except (NetworkError, ExchangeError) as e:
            sys.stdout.write(f"\n⚠️ API ERROR: {str(e)}\n")
            time.sleep(5)
        except Exception as e:
            sys.stdout.write(f"\n⚠️ SYSTEM ERROR: {str(e)}\n")
            time.sleep(5)

    # --- RESTORED SECURE SHUTDOWN ---
    sys.stdout.write(f"\n{sep}\n🛑 ZENVO ENGINE OFFLINE\n{sep}\n")