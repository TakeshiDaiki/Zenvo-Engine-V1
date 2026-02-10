### 🚀 Zenvo Engine V1 – Algorithmic Trend-Following Trading System

Zenvo Engine is a high-performance algorithmic trading system designed for Binance Spot markets.
It implements a **Trend-Follower Rebound strategy**, combining momentum confirmation with corrective
entry logic to capture high-probability rebounds in bullish conditions.

The system focuses on **capital protection**, **trend continuation**, and **resilient execution**
through a dynamic trailing ecosystem and fault-tolerant architecture.

---

### 🧠 Strategy Profile – Trend-Follower Rebound

Zenvo Engine is designed to enter trades **after corrective pullbacks within an active bullish trend**,
filtering market noise and avoiding euphoric price peaks.

#### Entry Logic

- **Momentum Filter**
  - Price must be above **EMA 9**
  - Confirms immediate bullish strength

- **Rebound Filter**
  - **RSI ≤ 40**
  - Ensures entry occurs after a controlled correction, not at market tops

This combination allows the bot to enter **with the trend, but not late**.

---

### 🧠 Dynamic Position Management

Zenvo Engine uses a fully dynamic exit system that adapts to price evolution in real time,
allowing profits to run while protecting capital.

#### Dynamic Trailing Loss (Protection)

- Active immediately after purchase
- Tracks the highest price reached (`max_price`)
- Exit level is recalculated **1.5% below the peak**
- Locks in gains and limits downside on reversals

#### Dynamic Trailing Profit (Trend Expansion)

- Activated once price reaches **+3.0%**
- Enables aggressive trend-following behavior
- Position is closed only if price retraces **1.5% from the new high**

This system avoids fixed take-profits and adapts naturally to market conditions.

---

### 🌍 Market Explorer (High Liquidity Assets)

Zenvo Engine includes optimized access to **20 high-liquidity Binance Spot pairs** to ensure
tight spreads, fast execution, and reliable order fills:

**Trading Pairs**

- BTC/USDT                   
- ETH/USDT
- BNB/USDT
- SOL/USDT
- XRP/USDT
- ADA/USDT
- AVAX/USDT
- DOGE/USDT
- DOT/USDT
- MATIC/USDT
- LINK/USDT
- SHIB/USDT
- LTC/USDT
- TRX/USDT
- NEAR/USDT
- ATOM/USDT
- UNI/USDT
- ICP/USDT
- APT/USDT
- OP/USDT

---

### ⚙️ Technical Features

- **Thread-Safe Architecture**  
  Trading logic runs in a separate thread, preventing GUI freezes during order execution.

- **Fail-Safe Position Recovery**  
  If a temporary Binance connection issue occurs after a buy order, the bot preserves entry
  data in memory and resumes position tracking automatically.

- **Null Data Protection**  
  Candlestick data is validated before indicator calculations to prevent crashes caused by
  incomplete or missing klines.

- **High Availability**  
  Handles network and exchange exceptions without terminating execution.

- **Real-Time Monitoring**  
  Professional terminal output displaying live PnL, drawdown (DD), and tracked peak price.

---

### 🖥️ User Interface (UX)

- Dark Mode optimized for long trading sessions
- Anti-flicker terminal buffer for stable real-time visualization
- Automatic mode switching:
  - **Waiting Mode**
  - **Position Management Mode** (live DD & Profit display)
- Persistent favorites system using `favorites.json`

---

### 🛠️ Technology Stack

- **Language:** Python 3.10+
- **Data Processing:** Pandas
- **Exchange API:** CCXT (Binance)
- **Build System:** PyInstaller

---

### 📦 Installation & Setup

**Clone the repository**
```bash
git clone https://github.com/TakeshiDaiki/Zenvo-Engine-V1
cd Zenvo-Engine-V1
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the bot
```bash
python gui.py
```

#### 📁 Project Structure
```text
Binance_Bot/
├── core/                # Core connectivity modules
│   ├── exchange.py      # Binance API and order management
│   ├── risk.py          # Risk management logic
│   └── __init__.py
├── logic/               # Trading logic
│   ├── indicators.py    # RSI, EMA and metrics calculations
│   ├── strategy.py      # Entry and exit definitions
│   └── __init__.py
├── gui.py               # Graphical user interface
├── main.py              # Engine orchestrator
├── config.py            # Global configurations
├── .env                 # Private credentials
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── LICENSE              # MIT License
```
#### 📄 License

This project is released under the MIT License.
You are free to use, modify, and distribute it.

#### 👤 Author

**Jose Salazar**

**GitHub:** https://github.com/TakeshiDaiki

**LinkedIn:**

#### ⚠️ Disclaimer

This software is a technical demonstration and research tool.
Trading digital assets involves significant risk.
The author assumes no responsibility for financial losses incurred through the use of this system.
Trade responsibly.
