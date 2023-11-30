import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import markdown
import lxml.html
from lxml import etree
import os
from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,
                          ColumnDataSource, OpenURL, TapTool)
from bokeh.plotting import from_networkx, figure, output_file, show

all_links = set()
hyperlinks = dict()

for eachpath in Path('./files').rglob('*.md'):
    
    with open(eachpath) as each_file:
        markdown_string1 = each_file.read()

        html_string1 = markdown.markdown(markdown_string1)
        
        try:
            doc1 = lxml.html.fromstring(html_string1)
        except etree.ParserError:
            continue

        if not doc1.xpath('//h1'):
            continue

        doc_heading1 = doc1.xpath('//h1')[0].text

        hyperlinks[doc_heading1] = eachpath.resolve().as_posix()

        for link in doc1.xpath('//a'):
            linked_file = link.get('href')
            abs_linked_path = (eachpath.parent / linked_file).resolve()

            if not os.path.exists(abs_linked_path):
                continue

            with open(abs_linked_path) as linkedfile:
                markdown_string2 = linkedfile.read()
                html_string2 = markdown.markdown(markdown_string2)
                doc2 = lxml.html.fromstring(html_string2)

                doc_heading2 = doc2.xpath('//h1')[0].text

                all_links.add((doc_heading1, doc_heading2))

print(hyperlinks)

g = nx.DiGraph()

g.add_edges_from(all_links)

nx.set_node_attributes(g, hyperlinks, "FILE_LOCATION")

p = figure(width=400, height=400,
           x_range=Range1d(-2, 6), y_range=Range1d(-0.2, 0.5),
           tools="tap", title="Click the URL")
node_hover_tool = HoverTool(tooltips=[("URL", "@URL")])
url = "@URL"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

# pos = nx.spring_layout(g)

mapping = dict((n, i) for i, n in enumerate(g.nodes))
H = nx.relabel_nodes(g, mapping)

graph_renderer = from_networkx(H, nx.spring_layout, scale=0.5, center=(0, 0))

graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="white", 
                                           line_color = "black", line_width = 1)
graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=1, 
                                               line_width=1)
p.renderers.append(graph_renderer)

output_file("interactive_graphs.html")
show(p)

