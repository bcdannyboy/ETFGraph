import networkx as nx

def find_influential_stocks(G):
    """
    Find the top 10 most and least influential stocks based on centrality measures.
    
    Args:
        G (nx.Graph): A NetworkX graph of stocks and ETFs.
        
    Returns:
        tuple: Returns two lists containing the top 10 most and least influential stocks, respectively.
    """
    # Calculate centrality for the graph
    centrality = nx.degree_centrality(G)
    
    # Filter centrality to include only stock nodes
    stock_centrality = {node: cent for node, cent in centrality.items() if G.nodes[node]['type'] == 'Stock'}
    
    # Sort stocks by centrality
    sorted_stocks = sorted(stock_centrality.items(), key=lambda item: item[1], reverse=True)
    
    # Top 10 most influential stocks
    top_most_influential = sorted_stocks[:10]
    
    # Top 10 least influential stocks
    top_least_influential = sorted_stocks[-10:]
    
    return top_most_influential, top_least_influential
