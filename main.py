import graph_builder.src as src
from pathlib import Path

if __name__=="__main__":
    print("RUNNING GRAPH BUILDER...\n--------------------------------------------\n")
    try:
        folder = src.GraphedDirectory(Path("./files"))
        details = folder.graph_details
        print("\n--------------------------------------------\nNODES: ")
        print(f"\t{details['nodes']}")
        print("EDGES")
        for edge in details['edges']:
            print(f"\t{edge}")
    except src.GraphBuilderError as e:
        print(f"\n--------------------------------------------\nERROR - TERMINATING: {e.message}")
