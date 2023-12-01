import graph_builder.src as src
from pathlib import Path

if __name__=="__main__":
    data = src.all_headings_and_links(Path("./files"))
    nodes_and_edges = {
        "nodes": src.get_nodes(data),
        "edges": src.get_edges(data)
    }

    print("NODES: ")
    print(f"\t{nodes_and_edges['nodes']}")
    print("EDGES")
    for edge in nodes_and_edges['edges']:
        print(f"\t{edge}")