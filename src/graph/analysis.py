
def stocks_with_most_weight(G):
    """
    stocks_with_most_weight returns a list of stocks sorted by the total weight of their connections.
    
    Args:
        G (nx.Graph): The graph to analyze.
        
    Returns:
        list: A list of tuples containing the stock name and the total weight of its connections, sorted in descending order.
    """
    stock_weights = {}
    for u, v, data in G.edges(data=True):
        if G.nodes[u]['type'] == 'Stock':
            stock = u
        elif G.nodes[v]['type'] == 'Stock':
            stock = v
        else:
            continue
        
        if stock not in stock_weights:
            stock_weights[stock] = 0
        stock_weights[stock] += data['weight']
    
    # Sort stocks by total weight
    sorted_stocks = sorted(stock_weights.items(), key=lambda item: item[1], reverse=True)
    return sorted_stocks

def stocks_with_most_inclusions(G):
    """
    stocks_with_most_inclusions returns a list of stocks sorted by the number of inclusions in ETFs.
    
    Args:
        G (nx.Graph): The graph to analyze.
        
    Returns:
        list: A list of tuples containing the stock name and the number of inclusions in ETFs, sorted in descending order.
    """
    stock_counts = {}
    for node, data in G.nodes(data=True):
        if data['type'] == 'Stock':
            stock_counts[node] = G.degree(node)
    
    # Sort stocks by the number of inclusions
    sorted_stocks = sorted(stock_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_stocks

def analyze_etf_types(G):
    """
    Analyzes leveraged and inverse ETFs to determine their influence on stock nodes and market sentiment.
    
    Args:
        G (nx.Graph): The graph to analyze.
        
    Returns:
        dict: Returns a dictionary with keys 'leveraged', 'inverse' and 'standard' pointing to lists of stocks influenced by these ETF types.
    """
    etf_influence = {'leveraged': [], 'inverse': [], 'standard': []}
    for node, data in G.nodes(data=True):
        if data['type'] == 'ETF':
            # Collect all stocks linked to this ETF
            stocks = [nbr for nbr in G[node] if G.nodes[nbr]['type'] == 'Stock']
            if data['leveraged']:
                etf_influence['leveraged'].extend(stocks)
            elif data['inverse']:
                etf_influence['inverse'].extend(stocks)
            else:
                etf_influence['standard'].extend(stocks)

    # Remove duplicates by converting lists to sets and back to lists
    for key in etf_influence:
        etf_influence[key] = list(set(etf_influence[key]))

    return etf_influence

def sentiment_analysis_by_etf_type(etf_influence):
    """
    Perform a simple sentiment analysis based on the distribution of stocks in leveraged, inverse, and standard ETFs.
    
    Args:
        etf_influence (dict): Dictionary from analyze_etf_types function.
        
    Returns:
        dict: Sentiment scores indicating bullish or bearish tendencies.
    """
    sentiment_scores = {}
    # Assuming more stocks in leveraged ETFs suggests bullish market sentiment
    sentiment_scores['bullish'] = len(etf_influence['leveraged'])
    # Assuming more stocks in inverse ETFs suggests bearish market sentiment
    sentiment_scores['bearish'] = len(etf_influence['inverse'])

    return sentiment_scores
