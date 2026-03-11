"""
Financial Bonsai — Paper Trader
Runs MA20/MA50 daily strategy on live Kraken data with virtual money.
Run once per day. State persists between runs via JSON file.

Usage: python3 paper_trader.py
"""

import json
import os
from datetime import datetime
from kraken.spot import Market

# === CONFIGURATION ===
COINS = [
    ["BTC", "XBTEUR",  "XXBTZEUR"],
    ["ETH", "ETHEUR",  "XETHZEUR"],
    ["SOL", "SOLEUR",  "SOLEUR"],
]

STARTING_CAPITAL = 300.00   # Per coin
FEE_PCT = 0.40
MA_FAST = 20
MA_SLOW = 50
STATE_FILE = "paper_state.json"

client = Market()

def load_state():
    """Read the bot's notebook. If no notebook exists, create a fresh one."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)

    # First run — initialize fresh state for each coin
    state = {}
    for name, _, _ in COINS:
        state[name] = {
            "cash": STARTING_CAPITAL,
            "coins": 0.0,
            "position": "out",
            "last_signal": None,
            "trades": [],
        }
    return state


def save_state(state):
    """Write the bot's notebook to disk."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def fetch_daily_candles(pair, response_key):
    """Fetch daily OHLC candles from Kraken. Returns list of [datetime, close_price]."""
    raw = client.get_ohlc(pair=pair, interval=1440)
    candles = raw[response_key]
    prices = []
    for candle in candles:
        timestamp = int(candle[0])
        dt = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        close = float(candle[4])
        prices.append([dt, close])
    return prices


def get_signal(prices):
    """Calculate MA20/MA50 on the latest candle and return the signal."""
    if len(prices) < MA_SLOW:
        return None, None, None

    # MA on the last complete candle
    last = len(prices) - 1
    fast_ma = sum(p[1] for p in prices[last - MA_FAST + 1:last + 1]) / MA_FAST
    slow_ma = sum(p[1] for p in prices[last - MA_SLOW + 1:last + 1]) / MA_SLOW

    if fast_ma > slow_ma:
        signal = "BUY"
    elif fast_ma < slow_ma:
        signal = "SELL"
    else:
        signal = "HOLD"

    return signal, fast_ma, slow_ma

def execute_trade(coin_state, signal, price, coin_name):
    """Check for crossover and execute virtual trade if needed."""
    prev_signal = coin_state["last_signal"]
    coin_state["last_signal"] = signal

    # No previous signal yet — nothing to compare
    if prev_signal is None:
        return None

    # No crossover — signal hasn't changed
    if signal == prev_signal:
        return None

    today = datetime.now().strftime("%Y-%m-%d")

    # BUY: spend all cash
    if signal == "BUY" and coin_state["position"] == "out":
        fee = coin_state["cash"] * (FEE_PCT / 100)
        cash_after_fee = coin_state["cash"] - fee
        coins_bought = cash_after_fee / price
        coin_state["coins"] = coins_bought
        coin_state["cash"] = 0.0
        coin_state["position"] = "in"
        trade = {"type": "BUY", "date": today, "price": price, "coins": coins_bought, "fee": fee}
        coin_state["trades"].append(trade)
        return trade

    # SELL: convert all coins to cash
    if signal == "SELL" and coin_state["position"] == "in":
        gross = coin_state["coins"] * price
        fee = gross * (FEE_PCT / 100)
        cash = gross - fee
        coin_state["cash"] = cash
        coin_state["coins"] = 0.0
        coin_state["position"] = "out"
        trade = {"type": "SELL", "date": today, "price": price, "cash": cash, "fee": fee}
        coin_state["trades"].append(trade)
        return trade

    return None

# === MAIN ===

print("=== Financial Bonsai — Paper Trader ===")
print(f"Strategy: MA{MA_FAST}/MA{MA_SLOW} on daily candles")
print(f"Fee: {FEE_PCT}% per trade (Kraken taker)")
print(f"Capital: EUR {STARTING_CAPITAL:,.2f} per coin\n")

state = load_state()

for name, pair, key in COINS:
    print(f"--- {name} ---")

    # Fetch and analyze
    prices = fetch_daily_candles(pair, key)
    signal, fast_ma, slow_ma = get_signal(prices)
    current_price = prices[-1][1]
    current_date = prices[-1][0]

    if signal is None:
        print(f"  Not enough data for MA{MA_SLOW} yet.")
        print()
        continue

    # Execute trade if crossover detected
    coin_state = state[name]
    trade = execute_trade(coin_state, signal, current_price, name)

    # Display
    print(f"  Date:     {current_date}")
    print(f"  Price:    EUR {current_price:,.2f}")
    print(f"  MA{MA_FAST}:     EUR {fast_ma:,.2f}")
    print(f"  MA{MA_SLOW}:     EUR {slow_ma:,.2f}")
    print(f"  Signal:   {signal}")

    if trade:
        print(f"  >>> TRADE: {trade['type']} at EUR {current_price:,.2f} (fee: EUR {trade['fee']:.2f})")
    else:
        print(f"  No crossover — holding {coin_state['position']}.")

    # Portfolio value
    if coin_state["position"] == "in":
        value = coin_state["coins"] * current_price
    else:
        value = coin_state["cash"]

    pnl = (value - STARTING_CAPITAL) / STARTING_CAPITAL * 100
    total_trades = len(coin_state["trades"])

    print(f"  Portfolio: EUR {value:,.2f} ({pnl:+.2f}%) | Trades: {total_trades}")
    print()

save_state(state)
print("State saved. Run again tomorrow!")