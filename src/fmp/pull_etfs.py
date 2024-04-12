import random
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Semaphore, Timer

import requests

from .utils import analyze_etf_attributes

RATE_LIMIT = 150  # Maximum requests per minute
REQUEST_INTERVAL = 60 / RATE_LIMIT  # Interval between requests in seconds
TIMEOUT = 10  # Timeout for HTTP requests in seconds

# Create a semaphore that will allow a maximum of RATE_LIMIT tokens per minute
semaphore = Semaphore(RATE_LIMIT)
exit_flag = False  # Global flag to signal the timer to stop

def release_semaphore(semaphore, request_interval):
    """ Release the semaphore periodically until instructed to stop. """
    while not exit_flag:
        semaphore.release()
        time.sleep(request_interval)

def fetch_etf_holdings(etf, fmp_key):
    """
    Fetches holdings for a specific ETF and returns the data.
    """
    semaphore.acquire()  # Ensure we don't exceed the rate limit

    holdings_url = f"https://financialmodelingprep.com/api/v3/etf-holder/{etf['symbol']}?apikey={fmp_key}"
    try:
        response = requests.get(holdings_url, timeout=TIMEOUT)
        if response.status_code == 200:
            name = etf['name']
            leveraged, inverse = analyze_etf_attributes(name)
            return etf['symbol'], {
                "leveraged": leveraged,
                "inverse": inverse,
                "holdings": response.json()
            }

        error_msg = f"[!] Failed to get ETF positions for {etf['symbol']} - Status code: {response.status_code}, Response: {response.text}"
        print(error_msg)
        return etf['symbol'], None
    except requests.RequestException as e:
        print(f"[!] Request failed for {etf['symbol']}: {e}")
        return etf['symbol'], None

def pull_etf_positions(num, fmp_key, rate_limit=RATE_LIMIT):
    """
    Fetch ETF positions using a fixed number of threads, displaying progress and adhering to rate limits.
    The function also ensures proper rate-limiting via a semaphore that gets released at a specified interval.

    Args:
        num (int): The number of ETFs to analyze, -1 indicates all available ETFs.
        fmp_key (str): API key for Financial Modeling Prep API.
        rate_limit (int): The maximum number of requests per minute. Default is 150.

    Returns:
        dict: A dictionary with ETF symbols as keys and fetched data as values, or None if an error occurs.
    """
    global exit_flag
    request_interval = 60 / rate_limit  # Recalculate the interval based on the provided rate limit
    exit_flag = False  # Reset the exit flag in case the function is called multiple times
    timer = Timer(0, release_semaphore, args=(semaphore, request_interval))
    timer.start()

    try:
        list_url = f"https://financialmodelingprep.com/api/v3/etf/list?apikey={fmp_key}"
        response = requests.get(list_url, timeout=TIMEOUT)
        if response.status_code == 200:
            etf_list = response.json()
            etfs_to_analyze = random.sample(etf_list, num) if num != -1 else etf_list

            etf_details = {}
            total_etfs = len(etfs_to_analyze)
            etfs_processed = 0

            print(f"[+] Starting ETF analysis at a rate of {rate_limit} requests per minute...")

            with ThreadPoolExecutor(max_workers=min(10, os.cpu_count() * 2)) as executor:
                futures = {executor.submit(fetch_etf_holdings, etf, fmp_key): etf for etf in etfs_to_analyze}
                for future in as_completed(futures):
                    etf_symbol, data = future.result()
                    etfs_processed += 1
                    progress = (etfs_processed / total_etfs) * 100
                    sys.stdout.write(f"\r[?] Progress: {progress:.2f}% ({etfs_processed}/{total_etfs})")
                    sys.stdout.flush()
                    if data:
                        etf_details[etf_symbol] = data

            print(f"\n[+] Completed analysis for {etfs_processed} ETF{'s' if etfs_processed != 1 else ''}")
            return etf_details
        else:
            print(f"[!] Failed to retrieve ETF list - Status code: {response.status_code}, Response: {response.text}")
            return None
    finally:
        exit_flag = True  # Signal the timer to stop
        timer.cancel()
        timer.join()  # Wait for the timer thread to actually finish
