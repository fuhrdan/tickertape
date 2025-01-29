import tkinter as tk
from tkinter import ttk
import yfinance as yf
from threading import Thread
import time

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        current = stock.history(period="1d").iloc[-1]
        return {
            "Current Price": current['Close'],
            "Open Price": current['Open'],
            "Day Low": current['Low'],
            "Day High": current['High'],
            "Prev Open": hist.iloc[-2]['Open'] if len(hist) > 1 else "N/A",
            "Prev Close": hist.iloc[-2]['Close'] if len(hist) > 1 else "N/A"
        }
    except Exception as e:
        return {"Error": str(e)}

def update_data():
    while True:
        for i, ticker in enumerate(ticker_entries):
            symbol = ticker.get().upper()
            if symbol:
                data = fetch_stock_data(symbol)
                for j, key in enumerate(stats_labels.keys()):
                    text = f"{key}: {data.get(key, 'N/A')}"
                    stats_labels[key][i].config(text=text)
        time.sleep(10)  # Update every 10 seconds

def start_update_thread():
    thread = Thread(target=update_data, daemon=True)
    thread.start()

# GUI Setup
root = tk.Tk()
root.title("Stock Tracker")
root.geometry("600x400")

ticker_entries = []

# Input fields for stock tickers
for i in range(5):
    ttk.Label(root, text=f"Ticker {i+1}:").grid(row=i, column=0, padx=5, pady=5)
    entry = ttk.Entry(root, width=10)
    entry.grid(row=i, column=1, padx=5, pady=5)
    ticker_entries.append(entry)

# Display labels
stats_labels = {key: [] for key in ["Current Price", "Open Price", "Day Low", "Day High", "Prev Open", "Prev Close"]}
for i, key in enumerate(stats_labels.keys()):
    ttk.Label(root, text=key).grid(row=0, column=i+2, padx=5, pady=5)
    for j in range(5):
        lbl = ttk.Label(root, text="N/A")
        lbl.grid(row=j+1, column=i+2, padx=5, pady=5)
        stats_labels[key].append(lbl)

# Start auto update
start_update_thread()
root.mainloop()
