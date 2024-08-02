from scraper import scrape_and_store
import time

def run_scraper():
    currency_pairs = [('GBP', 'INR'), ('AED', 'INR')]
    periods = ['1W', '1M', '3M', '6M', '1Y']

    for from_currency, to_currency in currency_pairs:
        for period in periods:
            try:
                scrape_and_store(from_currency, to_currency, period)
            except Exception as e:
                print(f"Error scraping {from_currency}/{to_currency} ({period}): {e}")
            time.sleep(5)  # Add a small delay between requests

if __name__ == '__main__':
    run_scraper()