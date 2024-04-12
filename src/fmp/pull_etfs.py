import random
import requests

from fmp.utils import analyze_etf_attributes

def pull_etf_positions(num, fmp_key):
    """
    pull_etf_positions pulls ETF positions from the Financial Modeling Prep API.
    
    Args:
        num (int): The number of ETFs to pull.
        fmp_key (str): The API key for the Financial Modeling Prep API.
        
    Returns:
        dict | None: A dictionary containing the ETF positions as returned by the API or None if the request failed.
    """    
    list_url = f"https://financialmodelingprep.com/api/v3/etf/list?l&apikey={fmp_key}"
    
    r1 = requests.get(list_url)
    if r1.status_code < 300 and r1.status_code >= 200:
        etf_list = r1.json()
        
        etfs_to_analyze = random.sample(etf_list, num) if num != -1 else etf_list
        etf_details = {}
        for etf in etfs_to_analyze:
            holdings_url = f"https://financialmodelingprep.com/api/v3/etf-holder/{etf['symbol']}?apikey={fmp_key}"
            r2 = requests.get(holdings_url)
            name = etf['name']
            leveraged, inverse = analyze_etf_attributes(name)
            if r2.status_code < 300 and r2.status_code >= 200:
                etf_details[etf['symbol']] = {
                    "leveraged": leveraged,
                    "inverse": inverse,
                    "holdings": r2.json(),
                }
            else:
                print(f"[!] Failed to get ETF positions for {etf['symbol']}: Got status code {r2.status_code}")
            
    return None