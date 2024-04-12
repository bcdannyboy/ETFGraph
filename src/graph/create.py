import networkx as nx

def create_graph_from_fmp(fmp_details):
    """
    create_graph_from_fmp creates a graph from the ETF positions returned by the Financial Modeling Prep API.
    
    Args:
        fmp_details (dict): A dictionary containing the ETF positions as returned by the API.
        
    Returns:
        nx.Graph: A NetworkX graph representing the ETFs and their positions.
    """
    
    if fmp_details is None:
        print("[!] Failed to create graph from FMP details: No details provided")
        return None
    
    G = nx.Graph()

    # Loop through each ETF and their details
    for etf_symbol, etf_data in fmp_details.items():
        # Extract ETF symbol and its holdings
        leveraged = etf_data['leveraged']
        inverse = etf_data['inverse']
        holdings = etf_data['holdings']
        
        # Add ETF node if it's not already added
        if not G.has_node(etf_symbol):
            G.add_node(etf_symbol, type='ETF', leveraged=leveraged, inverse=inverse)

        # Loop through each stock in the holdings
        for stock in holdings:
            stock_symbol = stock['asset']
            weight = stock['weightPercentage']

            # Add stock node if it's not already added
            if not G.has_node(stock_symbol):
                G.add_node(stock_symbol, type='Stock')

            # Add an edge between the ETF and the stock
            G.add_edge(etf_symbol, stock_symbol, weight=weight)

    return G
