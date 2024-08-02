import requests
from bs4 import BeautifulSoup
import datetime
import time
from database import get_db_connection
import json

def scrape_yahoo_finance(from_currency, to_currency, period):
    quote = f"{from_currency}{to_currency}=X"
    end_date = int(time.time())
    
    if period == '1W':
        start_date = end_date - 7 * 24 * 60 * 60
    elif period == '1M':
        start_date = end_date - 30 * 24 * 60 * 60
    elif period == '3M':
        start_date = end_date - 90 * 24 * 60 * 60
    elif period == '6M':
        start_date = end_date - 180 * 24 * 60 * 60
    elif period == '1Y':
        start_date = end_date - 365 * 24 * 60 * 60
    else:
        raise ValueError("Invalid period")

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{quote}?period1={start_date}&period2={end_date}&interval=1d"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return []

    try:
        data = response.json()
        timestamps = data['chart']['result'][0]['timestamp']
        close_prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
        
        forex_data = []
        for timestamp, close_price in zip(timestamps, close_prices):
            date = datetime.datetime.fromtimestamp(timestamp).date()
            if close_price is not None:
                forex_data.append((date, close_price))
        
        return forex_data
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON data: {e}")
        return []

def store_data(from_currency, to_currency, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for date, rate in data:
        cursor.execute("""
            INSERT OR REPLACE INTO forex_rates (from_currency, to_currency, date, rate)
            VALUES (?, ?, ?, ?)
        """, (from_currency, to_currency, date, rate))
    
    conn.commit()
    conn.close()

def scrape_and_store(from_currency, to_currency, period):
    data = scrape_yahoo_finance(from_currency, to_currency, period)
    if data:
        store_data(from_currency, to_currency, data)
        print(f"Scraped and stored {len(data)} records for {from_currency}/{to_currency} ({period})")
    else:
        print(f"No data scraped for {from_currency}/{to_currency} ({period})")

if __name__ == '__main__':
    # Test scraping
    scrape_and_store('GBP', 'INR', '1M')
    scrape_and_store('AED', 'INR', '1M')