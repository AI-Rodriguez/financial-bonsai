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
| **Phase 4.5** | ✅ Complete | Multi-strategy backtesting: MA7/21, MA20/50, MA50/200 across hourly, 4-hour, and daily candles |
| **Phase 5** | 📋 Planned | Paper trading — simulate real trades with virtual money |
| **Phase 6** | 📋 Planned | Live trading with small amounts (EUR 50–100) |
| **Phase 7** | 🔭 Horizon | AI-powered signals — sentiment analysis from news headlines |

## Key Findings

### Phase 4 — The Fee Problem

The MA7/MA21 crossover strategy **beat buy & hold** during a bear market (all three coins were down 21–28%) by limiting losses. But **trading fees were the dominant factor** — at Kraken's 0.40% taker rate, 16–20 round trips consumed 12–15% of capital, turning a damage-limiting strategy into a net loser.

**The lesson:** trading frequency is the enemy of profitability when fees are factored in.

| Coin | Strategy Return | Buy & Hold | Difference | Fees Paid |
|------|----------------|------------|------------|-----------|
| BTC  | -13.52%        | -21.99%    | +8.48%     | €44.15    |
| ETH  | -18.03%        | -28.38%    | +10.35%    | €39.45    |
| SOL  | -4.34%         | -28.88%    | +24.54%    | €36.12    |

*Backtest period: Jan 31 – Mar 2, 2026 · 721 hourly candles per coin · Starting capital: €300 per coin*

### Phase 4.5 — The Window Size Hypothesis

If fees kill profitability through trade frequency, can wider MA windows reduce the number of trades enough to make the strategy viable? We tested three strategies across three timeframes — 27 backtests total.

**The golden cross (MA50/MA200) mostly failed.** It reduced trades to 1–4 per backtest and fees to €2–5, but the signals were so delayed that by the time it said "buy," the trend was already mature, and by the time it said "sell," the crash was already underway. Too smooth, too slow.

**The sweet spot was the middle: MA20/MA50 on daily candles.** One configuration — ETH daily MA20/MA50 — returned **+27.94%** over two years with just 5 round trips and €15.93 in fees. It caught two sustained rallies (+59.13% and +28.78%) and avoided the worst of the drawdowns.

| Coin | Time | Strategy | Trades | Fees | Return | B&H | Diff |
|------|------|----------|--------|------|--------|-----|------|
| BTC | daily | MA50/MA200 | 2 | €5.19 | +4.38% | +0.10% | +4.29% |
| ETH | daily | MA20/MA50 | 5 | €15.93 | **+27.94%** | -45.83% | **+73.77%** |
| SOL | 4-hour | MA20/MA50 | 6 | €12.88 | -11.15% | -45.18% | +34.03% |

*Selected results from 27 backtests. Full comparison in backtest.py output.*

### What We Learned

**Self-similarity in markets.** When we first compared timeframes, the trade count was suspiciously similar — 18, 19, 20 trades regardless of whether the candles were hourly or daily. This isn't the exchange gaming the system. It's a mathematical property: the density of trend reversals stays roughly constant across timescales. Financial markets exhibit fractal-like behavior — the pattern looks similar whether you zoom in or zoom out.

**Window size matters more than timeframe.** The original hypothesis was that longer candles (4-hour, daily) would fix the fee problem by producing fewer signals. But 720 candles produce roughly the same number of MA crossovers regardless of interval. What actually reduced trade count was widening the MA windows — MA20/MA50 produced 5–9 trades where MA7/MA21 produced 16–20.

**Same strategy, different asset, wildly different results.** ETH daily MA20/MA50 returned +27.94%. SOL daily MA20/MA50 lost 57.47%. Same logic, same timeframe, opposite outcomes. This tells us something fundamental: price-based strategies like MA crossover treat the market as a closed system — just numbers moving. But the market is an open system, driven by external forces: news, sentiment, regulation, adoption. The strategy can only react to price movements. It has no idea *why* the price moved. This is the argument for eventually adding sentiment analysis.

**Data mining bias is real.** We tested 27 combinations and found one clear winner. That could be genuine signal, or it could be statistical luck — test enough combinations and something will look great by chance. The broader structural insight (medium windows on daily candles outperform fast strategies on short timeframes) is more trustworthy than any single result.

## Tech Stack

- **Language:** Python 3.13
- **Exchange:** [Kraken](https://www.kraken.com/) (Binance is unavailable in the Netherlands)
- **SDK:** [python-kraken-sdk](https://pypi.org/project/python-kraken-sdk/) 3.2.7
- **Hardware:** MacBook Air (Apple Silicon)

## Project Structure

```
financial-bonsai/
├── bonsai.py              # Live monitoring bot (v5) — MA7/MA21 crossover signals
├── download_history.py    # Downloads OHLC candles from Kraken (hourly, 4-hour, daily)
├── backtest.py            # Multi-strategy backtester — MA7/21, MA20/50, MA50/200
├── requirements.txt       # Python dependencies
├── bonsai_log.csv         # Live data log (generated at runtime)
├── history_*_60m.csv      # Hourly candle data (generated)
├── history_*_240m.csv     # 4-hour candle data (generated)
├── history_*_1440m.csv    # Daily candle data (generated)
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

# Download historical data (hourly, 4-hour, and daily candles)
python3 download_history.py

# Run the multi-strategy backtester
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
- **Self-similarity** — financial markets exhibit fractal-like behavior across timescales
- **Data mining bias** — testing many combinations will produce winners by chance; structural insights matter more than individual results
- **Financial fundamentals** — DCA, compounding, ETFs, portfolio allocation

## Disclaimer

This is a personal learning project. Nothing here is financial advice. The strategies implemented are educational explorations, not recommendations. Always do your own research and consult professionals before making financial decisions.

## License

MIT — use it, learn from it, grow your own bonsai. 🌱
