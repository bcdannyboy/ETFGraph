import networkx as nx

def create_graph_from_fmp(fmp_details):
    """
    create_graph_from_fmp creates a graph from the ETF positions returned by the Financial Modeling Prep API.
    
    Args:
        fmp_details (map): A dictionary containing the ETFs mapped to the list of positions as returned by the API.
        
    Returns:
        nx.Graph: A NetworkX graph representing the ETFs and their positions.
    """
    
    G = nx.Graph()

    # Loop through each ETF and their positions
    for etf, positions in fmp_details.items():
        # Add ETF node if it's not already added
        if not G.has_node(etf):
            G.add_node(etf, type='ETF')

        # Loop through each stock in the positions list
        for position in positions:
            stock = position['asset']
            weight = position['weightPercentage']

            # Add stock node if it's not already added
            if not G.has_node(stock):
                G.add_node(stock, type='Stock')

            # Add an edge between the ETF and the stock
            # The weight on the edge is the weightPercentage of the stock in the ETF
            G.add_edge(etf, stock, weight=weight)

    return G
