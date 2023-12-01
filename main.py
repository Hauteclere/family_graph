import src
from pathlib import Path
from bokeh.models import ColumnDataSource, OpenURL, TapTool
from bokeh.plotting import figure, output_file, show

if __name__=="__main__":
    data = src.all_headings_and_links(Path("./files"))
    nodes_and_edges = {
        "nodes": src.get_nodes(data),
        "edges": src.get_edges(data)
    }

    output_file("test.html")

    p = figure(width=400, height=400,
               tools="tap", title="")
    
    source = ColumnDataSource(data=dict(
        x = [index for index, node in enumerate(nodes_and_edges["nodes"])],
        y = [index for index, node in enumerate(nodes_and_edges["nodes"])],
        color = ["red" for item in nodes_and_edges["nodes"]]
    ))

    p.circle('x', 'y', color='color', size=20, source=source)

    url = "http://www.google.com"

    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    show(p)
    
