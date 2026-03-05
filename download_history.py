"""
Financial Bonsai — Historical Data Downloader
Downloads OHLC (Open, High, Low, Close) candle data from Kraken.
Saves to CSV files for backtesting.

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

# 60 = hourly candles. Kraken returns up to 720 = ~30 days
INTERVAL = 60

print("=== Financial Bonsai — History Downloader ===")
print(f"Interval: {INTERVAL} minutes (hourly candles)")
print(f"Max candles: 720 (~30 days of hourly data)\n")

for name, pair, key in COINS:
    print(f"Downloading {name}...", end=" ")

    # Pull OHLC data from Kraken
    raw = client.get_ohlc(pair=pair, interval=INTERVAL)
    candles = raw[key]

    # Each candle is a list:
    # [timestamp, open, high, low, close, vwap, volume, count]

    filename = f"history_{name}_{INTERVAL}m.csv"

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
    print()

    # Small pause between requests to be polite to Kraken's servers
    time.sleep(1)

print("Done! Your historical data is ready for backtesting.")
