# Please be aware that this program can take upwards of 30 minutes to retrieve the stock information.

import tkinter as tk
from tkinter import ttk
import yfinance as yf
import pandas as pd
from threading import Thread
import time

def fetch_market_data():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "BRK-B", "JPM"]  # Example tickers
    stocks = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")  # Fetch past 2 days of data
            if len(hist) >= 2:
                open_price = hist['Open'][-1]
                close_price = hist['Close'][-1]
                high_price = hist['High'][-1]
                low_price = hist['Low'][-1]
                volatility = abs(open_price - close_price)
                stocks[ticker] = {
                    "Open": open_price,
                    "Close": close_price,
                    "High": high_price,
                    "Low": low_price,
                    "Volatility": volatility
                }
        except:
            continue
    
    return sorted(stocks.items(), key=lambda x: x[1]['Volatility'], reverse=True)[:10]

def update_loading_status():
    symbols = [".", "..", "..."]
    index = 0
    while loading_flag:
        loading_label.config(text=f"Loading{symbols[index]}")
        index = (index + 1) % len(symbols)
        time.sleep(0.5)

def update_estimated_time():
    estimated_time = 30  # Placeholder estimated time in seconds
    while estimated_time > 0 and loading_flag:
        time_label.config(text=f"Estimated time remaining: {estimated_time}s")
        time.sleep(1)
        estimated_time -= 1
    time_label.config(text="Data loaded.")

def update_data():
    global loading_flag
    loading_flag = True
    loading_thread = Thread(target=update_loading_status, daemon=True)
    loading_thread.start()
    time_thread = Thread(target=update_estimated_time, daemon=True)
    time_thread.start()
    
    top_stocks = fetch_market_data()
    for i, (ticker, data) in enumerate(top_stocks):
        ticker_labels[i].config(text=ticker)
        for j, key in enumerate(["Open", "Close", "High", "Low", "Volatility"]):
            stats_labels[key][i].config(text=f"{key}: {data[key]:.2f}")
    
    loading_flag = False
    loading_label.config(text="Data Loaded")

def start_update_thread():
    thread = Thread(target=update_data, daemon=True)
    thread.start()

# GUI Setup
root = tk.Tk()
root.title("Top 10 Most Volatile Stocks")
root.geometry("600x400")

ticker_labels = [ttk.Label(root, text="") for _ in range(10)]
stats_labels = {key: [ttk.Label(root, text="N/A") for _ in range(10)] for key in ["Open", "Close", "High", "Low", "Volatility"]}

for i in range(10):
    ticker_labels[i].grid(row=i+1, column=0, padx=5, pady=5)
    for j, key in enumerate(["Open", "Close", "High", "Low", "Volatility"]):
        stats_labels[key][i].grid(row=i+1, column=j+1, padx=5, pady=5)

# Loading Status
loading_flag = False
loading_label = ttk.Label(root, text="Loading.", font=("Arial", 12))
loading_label.grid(row=11, column=0, columnspan=6, pady=10)

time_label = ttk.Label(root, text="Estimated time remaining: 30s", font=("Arial", 10))
time_label.grid(row=12, column=0, columnspan=6, pady=5)

start_update_thread()
root.mainloop()
