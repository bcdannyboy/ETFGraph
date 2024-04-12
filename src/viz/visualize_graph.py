import matplotlib.pyplot as plt # type: ignore
import networkx as nx # type: ignore
import numpy as np # type: ignore

def plot_graph(G, partition=None):
    """
    plot_graph plots the provided NetworkX graph with optional partitioning.
    
    Args:
        G (nx.Graph): The NetworkX graph to plot.
        partition (dict, optional): A dictionary containing node names as keys and their community as values.
        
    Returns:
        None: The function plots the graph but does not return anything.
    """
    k_value = 1 / np.sqrt(G.number_of_nodes()) * 3  # Scale k with the inverse square root of the number of nodes, multiplied for more spacing

    # Position nodes using an improved spring layout
    pos = nx.spring_layout(G, k=k_value, iterations=100, seed=42)  # Increased k for spacing, more iterations for better positioning

    # Draw the graph
    plt.figure(figsize=(16, 12))  # Increased figure size for better visibility

    # If a partition is provided, color nodes according to their partition
    if partition:
        cmap = plt.get_cmap('viridis')  # Color map
        num_communities = len(set(partition.values()))
        colors = [cmap(i / num_communities) for i in range(num_communities)]
        
        for node, community in partition.items():
            node_size = G.degree(node) * 10  # Scale node size by degree to highlight more connected nodes
            nx.draw_networkx_nodes(G, pos, [node], node_size=node_size, node_color=[colors[community]])
    else:
        node_sizes = [G.degree(node) * 10 for node in G]  # Scale node sizes by degree
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')

    edge_widths = [0.1 + 0.5 * data['weight'] for _, _, data in G.edges(data=True)]  # Scale edge widths by weight
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    
    plt.title('Network Graph of ETFs and Stocks')
    plt.axis('off')  # Turn off the axis
    plt.show()