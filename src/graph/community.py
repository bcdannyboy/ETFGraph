import community as community_louvain
from cdlib import algorithms, evaluation, NodeClustering

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

def detect_communities_overlapping(G):
    """
    detect_communities_overlapping detects overlapping communities in a graph using the Label Propagation method.

    Args:
        G (nx.Graph): The graph to analyze.

    Returns:
        NodeClustering: A NodeClustering object containing the detected communities.
    """
    communities = algorithms.label_propagation(G)
    return communities

def community_modularity(G, communities):
    """
    Calculate the modularity score of the communities.

    Args:
        G (nx.Graph): The graph to analyze.
        communities (dict or NodeClustering): Community data.

    Returns:
        float: The modularity score.
    """
    # If communities is a dictionary, convert it to NodeClustering format
    if isinstance(communities, dict):
        # Create a list of communities from the dictionary
        community_list = {}
        for node, community_id in communities.items():
            if community_id not in community_list:
                community_list[community_id] = []
            community_list[community_id].append(node)
        communities = NodeClustering(list(community_list.values()), G, "Louvain")

    # Calculate modularity
    return evaluation.newman_girvan_modularity(G, communities).score