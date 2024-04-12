import community as community_louvain

def detect_communities_louvain(G):
    """
    detect_communities_louvain detects communities in a graph using the Louvain method.

    Args:
        G (nx.Graph): The graph to analyze.

    Returns:
        dict: A dictionary where keys are node names and values are their community.
    """
    # The function uses the Louvain method to detect communities
    partition = community_louvain.best_partition(G)
    # Returning the partition dictionary, where keys are node names and values are their community
    return partition
