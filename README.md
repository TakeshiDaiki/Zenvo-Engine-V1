### 🚀 Zenvo Engine V1 – Hybrid Algorithmic Trading System

Zenvo Engine is a high-performance trading system designed for Binance Spot markets.
It combines quantitative analysis with adaptive strategies to optimize entries and maximize profits using 
a dynamic Trailing Stop and Trailing Profit ecosystem.

### 🚀 Evolution of: Pantuflito-Bot

### 🧠 Dynamic Position Management

Unlike traditional bots with fixed parameters, Zenvo Engine implements dynamic position management to protect capital 
and let profits run:

#### Dynamic Trailing Loss (Protection)
From the moment of purchase, the bot tracks the highest price reached (max_price). 
The exit level is constantly recalculated 1.5% below the peak, 
automatically securing profits if the price continues rising.

#### Dynamic Trailing Profit (Harvesting)
Once the price reaches the activation target (3.0%), the bot enters “chase mode,”
allowing profits to grow and closing the position only when the market retraces 1.5% from its new high.

### 📊 Hybrid Entry Strategy

### Zenvo Engine adjusts its buy signal requirements according to market context:

| Component        |  Configuration |  Mode      |  Description                                              |
|------------------|----------------|------------|-----------------------------------------------------------|
| **EMA 200**      | Trend Filter   | Structural | Determines if the market is bullish or weak.              |
| **RSI (Hybrid)** | < 35.0         | **Hunter** | Activated in bullish trend (slow days / Uptrend).         |
| **RSI (Hybrid)** | < 30.0         | **Sniper** | Activated in bearish or sideways trends (maximum safety). |
| **Trailing Gap** | 1.5%           | Dynamic    | Distance from peak price to trigger sell.                 |
| **TP Trigger**   | 3.0%           | Dynamic    | Threshold to activate trend-following mode.               |


### ⚙️ Technical Features

**Adaptability in Low Volatility:** Increases sensitivity to capture short retracements in bullish markets.

**High Availability:**  Handles network (NetworkError) and exchange (ExchangeError) exceptions.

**Real-Time Monitoring:** Professional console with dynamic status line showing PnL and tracked peak price.

**Data Optimization:** Vectorized calculations with Pandas for ultra-fast indicator processing.

### 🛠️ Technology Stack

**Language:** Python 3.10+

**Data Science:** Pandas

**API Connector:** CCXT (Binance)

**Compilation:** PyInstaller

### 📦 Installation & Setup

**Clone the repository:**
```
git clone https://github.com/TakeshiDaiki/Binance_Boot.git
cd Binance_Boot
```

**Install dependencies:**
```
pip install -r requirements.txt
```

**Configure credentials:**

Add your API Keys to .env or inside the core/ module.

**Run the bot:**
```
python main.py
```

**Create a production executable (.exe):**
```
pyinstaller --noconfirm --onefile --windowed --name "Zenvo_Engine_V1" --add-data "core;core" --add-data "logic;logic" main.py
```
### 📁 Project Structure
```text
Binance_Bot/
├── core/                # Core connectivity modules
│   ├── exchange.py      # Binance API and order management
│   ├── risk.py          # Risk management logic
│   └── __init__.py
├── logic/               # Bot brain
│   ├── indicators.py    # RSI, EMA, and metrics calculations
│   ├── strategy.py      # Buy/sell signal definitions
│   └── __init__.py
├── gui.py               # Graphical user interface
├── main.py              # Main engine orchestrator
├── config.py            # Global configurations and parameters
├── .env                 # Private credentials
├── requirements.txt     # Required libraries
├── README.md            # Technical documentation
└── LICENSE              # MIT License
```
### 📄 License

This project is under the MIT License. You may use, modify, and distribute freely.

### 👤 Author

**Jose Salazar**
**GitHub:** https://github.com/TakeshiDaiki
**LinkedIn:** https://www.linkedin.com/in/jose-salazar

### ⚠️ Disclaimer

This software is a technical demonstration tool. Trading digital assets carries high risk. 
The author is not responsible for any financial decisions made using this algorithm. Trade with caution.