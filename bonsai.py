import time
import csv
from datetime import datetime
from collections import deque
from kraken.spot import Market

client = Market()

# Coin configuration: [display name, API pair, response key]
COINS = [
    ["BTC", "XBTEUR",  "XXBTZEUR"],
    ["ETH", "ETHEUR",  "XETHZEUR"],
    ["SOL", "SOLEUR",  "SOLEUR"  ],
]

open_prices = {"BTC": None, "ETH": None, "SOL": None}

# Deque for each coin — stores last 21 prices, oldest drops off automatically
price_history = {
    "BTC": deque(maxlen=21),
    "ETH": deque(maxlen=21),
    "SOL": deque(maxlen=21),
}

print("=== Financial Bonsai - Multi-Coin Dashboard ===")
print("Watching BTC, ETH, SOL every 60 seconds. Press Ctrl+C to stop.\n")

# Write CSV header once
with open("bonsai_log.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "coin", "price", "change_pct", "ma7", "ma21", "signal"])

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"--- {timestamp} ---")

    for name, pair, key in COINS:
        ticker = client.get_ticker(pair=pair)
        data = ticker[key]
        price = float(data["c"][0])

        if open_prices[name] is None:
            open_prices[name] = float(data["o"])

        change_pct = (price - open_prices[name]) / open_prices[name] * 100
        arrow = "▲" if change_pct >= 0 else "▼"

        # Add new price to history
        price_history[name].append(price)

        # Calculate MAs only when we have enough data
        history = price_history[name]

        if len(history) >= 21:
            ma7  = sum(list(history)[-7:])  / 7
            ma21 = sum(list(history)[-21:]) / 21

            if ma7 > ma21:
                signal = "BUY"
            elif ma7 < ma21:
                signal = "SELL"
            else:
                signal = "HOLD"

            ma_display = f"MA7 {ma7:,.2f}  MA21 {ma21:,.2f}  [{signal}]"

        elif len(history) >= 7:
            ma7  = sum(list(history)[-7:]) / 7
            ma21 = None
            signal = "waiting"
            ma_display = f"MA7 {ma7:,.2f}  MA21 --  [waiting for {21 - len(history)} more]"

        else:
            ma7  = None
            ma21 = None
            signal = "waiting"
            ma_display = f"[waiting for {21 - len(history)} more readings]"

        print(f"  {arrow} {name:<4} EUR{price:>10,.2f}   {change_pct:+.2f}%")
        print(f"       {ma_display}")

        with open("bonsai_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, name, f"{price:.2f}", f"{change_pct:.2f}",
                f"{ma7:.2f}" if ma7 else "",
                f"{ma21:.2f}" if ma21 else "",
                signal
            ])

    print()
    time.sleep(60)