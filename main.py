import time
from core.exchange import BinanceClient
from logic.indicators import add_indicators


# --- CORE ENGINE FUNCTION ---
def run_bot(config):
    """
    Main entry point for the trading logic.
    Includes safety filters to prevent the thread from dying after a buy order.
    """
    # Extraction of settings
    api_key = config.get('api_key')
    secret_key = config.get('secret_key')
    symbol = config.get('symbol', 'BTC/USDT')
    usd_amount = float(config.get('usd_amount', 11.0))
    tf = config.get('timeframe', '1m')
    user_sl = float(config.get('sl', 1.5))
    user_tp = float(config.get('tp', 3.0))
    mode = config.get('mode', 'testnet')
    gui_instance = config.get('instance')

    rsi_threshold = 40.0
    sep = "=" * 45

    try:
        # Initializing connection
        client_manager = BinanceClient(api_key=api_key, secret_key=secret_key, mode=mode)
        current_bal = client_manager.get_balance("USDT")

        # Startup Header
        print(f"\n{sep}")
        print("✅ AUTHENTICATION SUCCESSFUL")
        print(sep)
        print("🚀 ZENVO CORE ONLINE - TRADING MODE")
        print(sep)
        print(f"📊 MARKET: {symbol} | TF: {tf}")
        print(f"💵 INITIAL BALANCE: {current_bal:,.2f} USDT")
        print(f"💰 INVESTMENT: {usd_amount} USDT")
        print(f"🛡️ SL (Trailing Gap): {user_sl} % | 🎯 TP Activation: {user_tp} %")
        print(f"{sep}\n")

        # Position state variables
        in_position = False
        entry_price = 0
        max_price = 0
        trailing_activated = False

        # Main Trading Loop
        while gui_instance.bot_running:
            try:
                # 1. Fetch data and calculate indicators
                df = client_manager.get_klines(symbol, tf)
                if df is None or df.empty:
                    time.sleep(2)
                    continue

                df = add_indicators(df)
                rsi_val = df['rsi'].iloc[-1]
                ema_9_v = df['ema9'].iloc[-1]
                current_price = df['close'].iloc[-1]

                # 2. Entry Logic (If not in a trade)
                if not in_position:
                    if rsi_val <= rsi_threshold and current_price > ema_9_v:
                        print(f"\n🎯 SIGNAL DETECTED: RSI {rsi_val:.2f} | Price > EMA 9")
                        if client_manager.create_order(symbol, 'buy', usd_amount):
                            entry_price = current_price
                            max_price = current_price
                            in_position = True
                            trailing_activated = False
                            print(f"🟢 BOUGHT @ {entry_price:,.2f} USDT")
                    else:
                        # Real-time monitoring line
                        print(
                            f"\r🕒 {time.strftime('%H:%M:%S')} | {symbol} | PR: {current_price:,.2f} | RSI: {rsi_val:.2f} | WAITING...",
                            end='')

                # 3. Position Management (If in a trade)
                else:
                    try:
                        # Update maximum price reached for trailing calculation
                        if current_price > max_price:
                            max_price = current_price

                        # Calculate PnL and Drawdown from peak
                        profit_pct = ((current_price - entry_price) / entry_price) * 100
                        drawdown = ((max_price - current_price) / max_price) * 100

                        # Status update while in position
                        status_msg = "TRAILING ACTIVE" if trailing_activated else "WAITING TP"
                        print(
                            f"\r📈 POS: {profit_pct:+.2f}% | MAX: {max_price:,.2f} | DD: {drawdown:.2f}% | {status_msg}",
                            end='')

                        # Step A: Check for Trailing Activation (Take Profit reached)
                        if not trailing_activated and profit_pct >= user_tp:
                            trailing_activated = True
                            print(f"\n🎯 TP REACHED! Trailing Stop Activated at {user_tp}% profit.")

                        # Step B: Check for Exit (Stop Loss or Trailing Stop hit)
                        if drawdown >= user_sl:
                            reason = "TRAILING STOP" if trailing_activated else "STOP LOSS"
                            print(f"\n🔴 SELLING: {reason} | Final PnL: {profit_pct:.2f}%")
                            if client_manager.create_order(symbol, 'sell', usd_amount):
                                in_position = False
                                trailing_activated = False
                                print(f"✅ POSITION CLOSED @ {current_price:,.2f} USDT")
                                print(f"{sep}\n")

                    except Exception as pos_err:
                        print(f"\n⚠️ POSITION MGMT ERROR: {pos_err}")

                time.sleep(1)  # 1-second scanning frequency

            except Exception as loop_err:
                print(f"\n⚠️ LOOP ERROR: {loop_err}")
                time.sleep(5)  # Wait before retrying on connection errors

        print("\n🛑 BOT STOPPED BY USER.")

    except Exception as crit_err:
        print(f"\n❌ CRITICAL ERROR: {crit_err}")