from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import requests
import sys
import time

from .utils import analyze_etf_attributes

RATE_LIMIT = 150  # Maximum requests per minute
REQUEST_INTERVAL = 60 / RATE_LIMIT  # Interval between requests in seconds

def fetch_etf_holdings(etf, fmp_key):
    """
    Fetches holdings for a specific ETF and returns the data.
    
    Args:
        etf (dict): A dictionary containing the ETF symbol and name.
        fmp_key (str): The API key for the Financial Modeling Prep API.
        
    Returns:
        tuple: A tuple containing the ETF symbol and a dictionary with the ETF data, or None if an error occurred.
    """
    time.sleep(REQUEST_INTERVAL)  # Sleep to ensure even distribution of requests
    holdings_url = f"https://financialmodelingprep.com/api/v3/etf-holder/{etf['symbol']}?apikey={fmp_key}"
    response = requests.get(holdings_url)
    if response.status_code == 200:
        name = etf['name']
        leveraged, inverse = analyze_etf_attributes(name)
        return etf['symbol'], {
            "leveraged": leveraged,
            "inverse": inverse,
            "holdings": response.json()
        }
    else:
        error_msg = f"[!] Failed to get ETF positions for {etf['symbol']} - Status code: {response.status_code}, Response: {response.text}"
        print(error_msg)
        return etf['symbol'], None

def pull_etf_positions(num, fmp_key):
    """
    Fetch ETF positions using a fixed number of threads, displaying progress and adhering to rate limits.
    
    Args:
        num (int): The number of ETFs to analyze. If -1, all ETFs will be analyzed.
        fmp_key (str): The API key for the Financial Modeling Prep API.
        
    Returns:
        dict: A dictionary containing the ETF symbols as keys and their data as values.
    """
    list_url = f"https://financialmodelingprep.com/api/v3/etf/list?apikey={fmp_key}"
    response = requests.get(list_url)
    if response.status_code == 200:
        etf_list = response.json()
        etfs_to_analyze = random.sample(etf_list, num) if num != -1 else etf_list

        etf_details = {}
        total_etfs = len(etfs_to_analyze)
        etfs_processed = 0

        print("[+] Starting ETF analysis...")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(fetch_etf_holdings, etf, fmp_key): etf for etf in etfs_to_analyze}
            for future in as_completed(futures):
                etf_symbol, data = future.result()
                etfs_processed += 1
                progress = (etfs_processed / total_etfs) * 100
                sys.stdout.write(f"\r[?] Progress: {progress:.2f}% ({etfs_processed}/{total_etfs})")
                sys.stdout.flush()
                if data:
                    etf_details[etf_symbol] = data

        print("\n[+] Completed analysis for all ETFs.")
        return etf_details
    else:
        print(f"[!] Failed to retrieve ETF list - Status code: {response.status_code}, Response: {response.text}")
        return None
