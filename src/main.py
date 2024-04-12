import random
from dotenv import load_dotenv
import os
import argparse
import src.fmp as fmp
import src.graph as graph

def init_etfgraph():
    """
    init_etfgraph initializes the ETF graph analysis tool.
    """
    print(f"Analyzing {args.num if args.num != -1 else 'all' } ETF{'s' if args.num != 1 else ''}...")
        
    etf_details = {}
    for etf in etfs_to_analyze:
        etf_details[etf] = fmp.pull_etf_positions(etf, FMPKey)
        
    etf_graph = graph.create_graph_from_fmp(etf_details)
        
if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(description="ETF Position Graph Analysis Tool")
    parser.add_argument('-n', '--num', type=int, help='The number of ETFs to analyze, if not provided all will be used', default=-1)
    args = parser.parse_args()
    
    FMPKey = os.getenv("FMPKey")
    
    if FMPKey is None:
        print("FMPKey not found")
        exit(-1)
        
    init_etfgraph()