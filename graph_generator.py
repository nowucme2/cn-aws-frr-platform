import networkx as nx
import matplotlib.pyplot as plt

def generate_network_graph(df, output_file):

    G = nx.DiGraph()

    for _, row in df.iterrows():
        if str(row.get("Rule Type", "")).lower() == "inbound":
            source = row.get("Source/Destination", "")
            target = row.get("Security Group", "")
            G.add_edge(source, target)

    # Create dark themed graph
    plt.figure(figsize=(14, 10), facecolor="black")

    pos = nx.spring_layout(G, k=0.6)

    nx.draw_networkx_nodes(
        G, pos,
        node_color="#00ff00",
        node_size=1200
    )

    nx.draw_networkx_edges(
        G, pos,
        edge_color="#00aa00",
        arrows=True
    )

    nx.draw_networkx_labels(
        G, pos,
        font_size=7,
        font_color="white"
    )

    plt.title("AWS Security Group Attack Graph", color="#00ff00")
    plt.axis("off")
    plt.savefig(output_file, facecolor="black")
    plt.close()
