# 🌱 Financial Bonsai

**A personal crypto trading bot built as a live learning laboratory.**

Small, controlled, actively tended and grown over time.  
Philosophy: start tiny, understand everything, scale with confidence.

> A bonsai — small by design, but alive, disciplined, and beautiful in its precision.

---

## What This Project Is

Financial Bonsai is a **market observatory** — a hands-on learning project where I build a crypto trading bot from scratch while teaching myself API integration, trading strategy, and financial literacy along the way.

Every line of code is written with understanding. Every decision is documented. Every mistake is data.

## Who I Am

I'm AI-Rodriguez — researcher in media theory, image and liberation politics based in Utrecht, Netherlands. Background in C and terminal usage. I started with zero trading knowledge and built this incrementally, one feature at a time.

## The Journey So Far

| Phase | Status | What I Built |
|-------|--------|-------------|
| **Phase 1** | ✅ Complete | Single coin price fetch, live loop, alerts, CSV logging |
| **Phase 2** | ✅ Complete | Multi-coin dashboard — BTC, ETH, SOL monitored simultaneously |
| **Phase 3** | ✅ Complete | Moving averages (MA7/MA21), crossover BUY/SELL/HOLD signals |
| **Phase 4** | ✅ Complete | Backtesting against 30 days of historical hourly data with fee simulation |
| **Phase 4.5** | 🔜 Next | Longer timeframes (4h, daily) to reduce trade frequency and fee impact |
| **Phase 5** | 📋 Planned | Paper trading — simulate real trades with virtual money |
| **Phase 6** | 📋 Planned | Live trading with small amounts (EUR 50–100) |
| **Phase 7** | 🔭 Horizon | AI-powered signals — sentiment analysis from news headlines |

## Key Insight from Backtesting

The MA7/MA21 crossover strategy **beat buy & hold** during a bear market (all three coins were down 21–28%) by limiting losses. But **trading fees were the dominant factor** — at Kraken's 0.40% taker rate, 16–20 round trips consumed 12–15% of capital, turning a damage-limiting strategy into a net loser.

**The lesson:** trading frequency is the enemy of profitability when fees are factored in.

| Coin | Strategy Return | Buy & Hold | Difference | Fees Paid |
|------|----------------|------------|------------|-----------|
| BTC  | -13.52%        | -21.99%    | +8.48%     | €44.15    |
| ETH  | -18.03%        | -28.38%    | +10.35%    | €39.45    |
| SOL  | -4.34%         | -28.88%    | +24.54%    | €36.12    |

*Backtest period: Jan 31 – Mar 2, 2026 · 721 hourly candles per coin · Starting capital: €300 per coin*

## Tech Stack

- **Language:** Python 3.13
- **Exchange:** [Kraken](https://www.kraken.com/) (Binance is unavailable in the Netherlands)
- **SDK:** [python-kraken-sdk](https://pypi.org/project/python-kraken-sdk/) 3.2.7
- **Hardware:** MacBook Air (Apple Silicon)

## Project Structure

```
financial-bonsai/
├── bonsai.py              # Live monitoring bot (v5) — MA7/MA21 crossover signals
├── download_history.py    # Downloads 720 hourly OHLC candles from Kraken
├── backtest.py            # MA7/MA21 strategy backtester with fee simulation
├── requirements.txt       # Python dependencies
├── bonsai_log.csv         # Live data log (generated at runtime)
├── history_BTC_60m.csv    # Historical BTC/EUR candle data (generated)
├── history_ETH_60m.csv    # Historical ETH/EUR candle data (generated)
├── history_SOL_60m.csv    # Historical SOL/EUR candle data (generated)
└── docs/
    └── session-summaries/ # PDF snapshots of each development session
```

## Getting Started

### Prerequisites

- Python 3.10+ (tested on 3.13)
- macOS or Linux (should work on Windows too)
- No Kraken API key needed for price monitoring and backtesting

### Installation

```bash
# Clone the repo
git clone https://github.com/AI-Rodriguez/financial-bonsai.git
cd financial-bonsai

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the live price monitor
python3 bonsai.py

# Download historical data (30 days of hourly candles)
python3 download_history.py

# Run the backtester
python3 backtest.py
```

Press `Ctrl+C` to stop the live monitor.

## Concepts I've Learned

Through building this project, I've gone from zero to understanding:

- **API integration** — REST APIs, SDKs, ticker data, OHLC candles
- **Moving Averages** — MA7 (fast) vs MA21 (slow), crossover strategy, lagging indicators
- **Backtesting** — testing strategies against historical data before risking real money
- **Trading fees** — maker vs taker, and how frequency amplifies fee impact
- **Signal noise & whipsaw** — why short timeframes generate unreliable signals
- **Financial fundamentals** — DCA, compounding, ETFs, portfolio allocation

## Disclaimer

This is a personal learning project. Nothing here is financial advice. The strategies implemented are educational explorations, not recommendations. Always do your own research and consult professionals before making financial decisions.

## License

MIT — use it, learn from it, grow your own bonsai. 🌱
