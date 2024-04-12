import json
import os
import pickle
import sys
import argparse

from dotenv import load_dotenv # type: ignore
from src import fmp
from src import graph
from src import viz


def init_etfgraph(num_etf=-1, display=False, rate_limit=150, output_file=None, graph_file=None):
    """
    init_etfgraph initializes and analyzes the ETF graph with detailed statistics and community analysis.
    It detects communities, identifies the largest ones, and analyzes the top stocks within these communities.
    It also performs various other analyses including ETF types, sentiment, and PageRank.
    Optionally outputs the results to a JSON file.
    
    Args:
        num_etf (int): The number of ETFs to analyze, if not provided all will be used.
        display (bool): Display the graph visualization.
        rate_limit (int): The rate limit for API requests (default 150/minute).
        output_file (str): Output file path for saving the results in JSON format.
        graph_file (str): Optional path to a pickled graph file to load instead of pulling data.
        
    Returns:
        nx.Graph: The ETF graph.
    
    Output:
        The function prints the analysis results and saves them to a JSON file if specified.
    """
    results = {}
    if graph_file:
        try:
            with open(graph_file, 'rb') as f:
                etf_graph = pickle.load(f)
            print("[+] Loaded graph from file.")
        except Exception as e:
            print(f"Error loading the graph from file: {e}")
            return
    else:
        etf_graph = graph.create_graph_from_fmp(fmp.pull_etf_positions(num_etf, FMPKey, rate_limit=rate_limit))
        if etf_graph is None:
            print("Failed to create graph. Exiting.")
            return

    communities = graph.detect_communities_louvain(etf_graph)
    community_size = {com: len([node for node in communities if communities[node] == com]) for com in set(communities.values())}
    largest_communities = sorted(community_size.items(), key=lambda x: x[1], reverse=True)[:5]

    community_results = {}
    print("[+] Analyzing top 5 largest communities:")
    for com, size in largest_communities:
        print(f"  Community {com} with {size} members")
        community_nodes = [node for node in etf_graph.nodes() if communities[node] == com]
        stock_weights = {node: sum(data['weight'] for u, v, data in etf_graph.edges(node, data=True) if etf_graph.nodes[u]['type'] == 'Stock' or etf_graph.nodes[v]['type'] == 'Stock') for node in community_nodes if etf_graph.nodes[node]['type'] == 'Stock'}
        top_stocks = sorted(stock_weights.items(), key=lambda item: item[1], reverse=True)[:10]
        community_results[com] = top_stocks
        print(f"  Top 10 stocks in Community {com}:")
        for stock, weight in top_stocks:
            print(f"    {stock}: {weight:.2f}")
    results['community_analysis'] = community_results

    etf_types = graph.analyze_etf_types(etf_graph)
    sentiment_scores = graph.sentiment_analysis_by_etf_type(etf_types)
    results['sentiment'] = sentiment_scores

    most_weight = graph.stocks_with_most_weight(etf_graph)[:10]
    most_inclusions = graph.stocks_with_most_inclusions(etf_graph)[:10]
    pagerank_scores = graph.perform_pagerank(etf_graph)
    top_pagerank = sorted(pagerank_scores.items(), key=lambda item: item[1], reverse=True)[:10]

    results['top_stocks_by_weight'] = most_weight
    results['top_stocks_by_inclusion'] = most_inclusions
    results['top_stocks_by_pagerank'] = top_pagerank

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"[+] Results saved to {output_file}")

    if display:
        print("[+] Visualizing ETF graph...")
        viz.plot_graph(etf_graph, communities)

    return etf_graph
  
if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(description="ETF Position Graph Analysis Tool")
    parser.add_argument('-n', '--num', type=int, help='The number of ETFs to analyze, if not provided all will be used', default=-1)
    parser.add_argument('-d', '--display', action='store_true', help='Display the graph visualization', default=False)
    parser.add_argument('-r', '--rate_limit', type=int, help='The rate limit for API requests (default 150/minute)', default=150)
    parser.add_argument('-o', '--output', type=str, help='Output file path for saving the results in JSON format')
    parser.add_argument('-s', '--save_graph', type=str, help='Output file path for saving the graph in pickle format')
    parser.add_argument('-l', '--load_graph', type=str, help='Input file path for loading a pickled graph')
    args = parser.parse_args()
    
    FMPKey = os.getenv("FMPKey")
    if FMPKey is None:
        print("FMPKey not found. Exiting.")
        sys.exit(-1)

    G = init_etfgraph(args.num, args.display, args.rate_limit, args.output, args.load_graph)
    
    if args.save_graph:
        print(f"[+] Saving graph to {args.save_graph}")
        with open(args.save_graph, 'wb') as f:
            pickle.dump(G, f)
            
    sys.exit(0)