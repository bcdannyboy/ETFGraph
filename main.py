import random
from dotenv import load_dotenv
import os
import argparse
import src.fmp as fmp
import src.graph as graph
import src.viz as viz

def init_etfgraph(display=False, rate_limit=150):
    """
    init_etfgraph initializes the ETF graph analysis tool.
    
    Args:
        display (bool): A boolean indicating whether to display the graph visualization.
        rate_limit (int): The rate limit for API requests (default 150/minute).
    """
    print(f"[+] Analyzing {args.num if args.num != -1 else 'all' } ETF{'s' if args.num != 1 else ''}...")
    
    etf_graph = graph.create_graph_from_fmp(fmp.pull_etf_positions(args.num, FMPKey, rate_limit=rate_limit))
        
    print(f"[+] Analyzed {args.num} ETF{'s' if args.num != 1 else ''} and {'their' if args.num != 1 else 'its'} positions")
    graph_communities = graph.detect_communities_louvain(etf_graph)
    
    print(f"[+] Detected {len(graph_communities)} communities in the ETF graph")
    
    etf_types = graph.analyze_etf_types(etf_graph)
    sentiment_by_etf_type = graph.sentiment_analysis_by_etf_type(etf_types)
    bull = sentiment_by_etf_type['bullish']
    bear = sentiment_by_etf_type['bearish']
    
    print(f"[+] Bull/Bear by ETF Type: {bull}/{bear} = {(bull / bear) if bear > 0 else 1.0 if bull > 0 else 0.0:.2f}")
    
    least_inclusions = graph.stocks_with_least_inclusions(etf_graph)
    most_inclusions = graph.stocks_with_most_inclusions(etf_graph)
    least_weight = graph.stocks_with_least_weight(etf_graph)
    most_weight = graph.stocks_with_most_weight(etf_graph)
    
    top_10_most_weight_tuple = sorted(most_weight, key=lambda x: x[1], reverse=True)[:10]
    top_10_least_weight_tuple = sorted(least_weight, key=lambda x: x[1])[:10]
    top_10_most_inclusions_tuple = sorted(most_inclusions, key=lambda x: x[1], reverse=True)[:10]
    top_10_least_inclusions_tuple = sorted(least_inclusions, key=lambda x: x[1])[:10]
    
    most_influential_tuple, least_influentia_tuple = graph.find_influential_stocks(etf_graph)

    most_influential = [stock for stock, centrality in most_influential_tuple]
    least_influential = [stock for stock, centrality in least_influentia_tuple]
    top_10_most_weight = [stock for stock, weight in top_10_most_weight_tuple]
    top_10_least_weight = [stock for stock, weight in top_10_least_weight_tuple]
    top_10_most_inclusions = [stock for stock, inclusions in top_10_most_inclusions_tuple]
    top_10_least_inclusions = [stock for stock, inclusions in top_10_least_inclusions_tuple]
    
    
    
    print(f"[+] Top 10 most influential stocks: {most_influential}")
    print(f"[+] Top 10 least influential stocks: {least_influential}")
    print(f"[+] Top 10 stocks with the most weight: {top_10_most_weight}")
    print(f"[+] Top 10 stocks with the least weight: {top_10_least_weight}")
    print(f"[+] Top 10 stocks with the most inclusions: {top_10_most_inclusions}")
    print(f"[+] Top 10 stocks with the least inclusions: {top_10_least_inclusions}")
    
    if display:
        print(f"[+] Visualizing ETF graph...")
        viz.plot_graph(etf_graph, graph_communities)
        
if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(description="ETF Position Graph Analysis Tool")
    parser.add_argument('-n', '--num', type=int, help='The number of ETFs to analyze, if not provided all will be used', default=-1)
    parser.add_argument('-d', '--display', action='store_true', help='Display the graph visualization')
    parser.add_argument('-r', '--rate_limit', type=int, help='The rate limit for API requests (default 150/minute)', default=150)
    args = parser.parse_args()
    
    FMPKey = os.getenv("FMPKey")
    
    if FMPKey is None:
        print("FMPKey not found")
        exit(-1)
        
    init_etfgraph(args.display, args.rate_limit)