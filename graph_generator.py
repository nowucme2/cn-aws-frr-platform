import networkx as nx
import matplotlib.pyplot as plt

def generate_network_graph(df, output_file="network_graph.png"):

    G = nx.DiGraph()

    for _, row in df.iterrows():
        rule_type = row.get("Rule Type", "").lower()
        source = row.get("Source/Destination", "")
        target = row.get("Security Group", "")

        if rule_type == "inbound":
            G.add_edge(source, target)

    plt.figure(figsize=(12,8))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=8)
    plt.title("AWS Security Group Attack Graph")
    plt.savefig(output_file)
    plt.close()

    return output_file
