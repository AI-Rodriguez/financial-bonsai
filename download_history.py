"""
Financial Bonsai — Historical Data Downloader
Downloads OHLC (Open, High, Low, Close) candle data from Kraken.
Saves to CSV files for backtesting.

Now downloads THREE timeframes per coin:
  60  = hourly candles   (~30 days of data)
  240 = 4-hour candles   (~120 days of data)
  1440 = daily candles   (~720 days / ~2 years of data)

Kraken returns up to 720 candles per request regardless of interval.

Usage: python3 download_history.py
No API key needed — this is public market data.
"""

import csv
import time
from datetime import datetime
from kraken.spot import Market

client = Market()

# Same coins as bonsai.py — same quirky key mapping
# [display_name, request_pair, response_key]
COINS = [
    ["BTC", "XBTEUR", "XXBTZEUR"],
    ["ETH", "ETHEUR", "XETHZEUR"],
    ["SOL", "SOLEUR", "SOLEUR"],
]

# Three timeframes to compare in backtesting
# [interval_minutes, human_label]
INTERVALS = [
    [60, "hourly"],
    [240, "4-hour"],
    [1440, "daily"],
]

print("=== Financial Bonsai — History Downloader ===")
print(f"Coins: {', '.join(c[0] for c in COINS)}")
print(f"Timeframes: {', '.join(t[1] for t in INTERVALS)}")
print(f"Max candles per request: 720\n")

for name, pair, key in COINS:
    print(f"--- {name} ---")

    for interval, label in INTERVALS:
        print(f"  Downloading {label} ({interval}m)...", end=" ")

        # Pull OHLC data from Kraken
        raw = client.get_ohlc(pair=pair, interval=interval)
        candles = raw[key]

        # Each candle is a list:
        # [timestamp, open, high, low, close, vwap, volume, count]

        filename = f"history_{name}_{interval}m.csv"

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "datetime", "open", "high", "low", "close", "vwap", "volume", "count"])

            for candle in candles:
                timestamp = int(candle[0])
                dt = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([
                    timestamp,
                    dt,
                    candle[1],  # open
                    candle[2],  # high
                    candle[3],  # low
                    candle[4],  # close
                    candle[5],  # vwap
                    candle[6],  # volume
                    candle[7],  # count (number of trades)
                ])

        # Quick summary
        total = len(candles)
        first_dt = datetime.fromtimestamp(int(candles[0][0])).strftime("%Y-%m-%d %H:%M")
        last_dt = datetime.fromtimestamp(int(candles[-1][0])).strftime("%Y-%m-%d %H:%M")
        first_close = float(candles[0][4])
        last_close = float(candles[-1][4])
        change = (last_close - first_close) / first_close * 100

        print(f"OK! {total} candles")
        print(f"    Period: {first_dt}  →  {last_dt}")
        print(f"    Price:  EUR {first_close:,.2f}  →  EUR {last_close:,.2f}  ({change:+.2f}%)")
        print(f"    Saved:  {filename}")

        # Small pause between requests to be polite to Kraken's servers
        time.sleep(1)

    print()

print("Done! Your historical data is ready for backtesting.")
