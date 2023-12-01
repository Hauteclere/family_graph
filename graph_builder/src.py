from pathlib import Path, PosixPath
import markdown
import lxml.html
import os
import re

all_edges = set()
hyperlinks = dict()

class NoHeadingError(ValueError):
    pass

def get_absolute_path(somepath: str, parent: PosixPath):
    if not len(somepath):
        return None
    if somepath[0] == "/":
        return somepath
    somepath = somepath.split('#')[0]
    return (parent / somepath).resolve()

def is_in_parent_folder(somepath: PosixPath, somefolder: PosixPath):
    return somefolder in Path(somepath).parents and os.path.exists(somepath)

def get_heading_from_doctree(doctree: lxml.html):
    headings = doctree.xpath('//h1')
    if not headings:
        raise NoHeadingError()
    return headings[0].text

def filter_to_local_links(links, localpath):
    return [
        locallink for locallink in (
            link for link in links
        ) if is_in_parent_folder(locallink, localpath.resolve())
    ]

def is_markdown_filepath(filepath: str):
    return (
        isinstance(filepath, str) and (
            bool(re.match(r".+\.md$", filepath)) or
            bool(re.match(r".+\.md#.+", filepath))
        )
    )
    
def absolute_links_from_doctree(doctree: lxml.html, filepath: PosixPath):
    return filter(
        lambda x: is_markdown_filepath(x),
        (
            get_absolute_path(
                eachlink.get('href'),
                filepath.parent.resolve()
            ) for eachlink in doctree.xpath('//a')
        )
    )

def heading_and_links_from_filepath(filepath: PosixPath, localpath: PosixPath):
    with open(filepath) as file:
        markdown_string = file.read()
        html_string = markdown.markdown(markdown_string)
        doctree = lxml.html.fromstring(html_string)
        
        all_links = absolute_links_from_doctree(
            doctree,
            filepath
        )
        
        return {
            "heading": get_heading_from_doctree(doctree),
            "links": filter_to_local_links(
                all_links, 
                localpath
            )
        }
        
def all_headings_and_links(somefolder: PosixPath):
    result = dict()
    
    for eachpath in somefolder.rglob('*.md'):
        try:
            result[eachpath.resolve()] = heading_and_links_from_filepath(eachpath, somefolder)
        except NoHeadingError:
            print(f"WARNING: file at {eachpath.resolve()} is malformed - no heading")
    return result

def get_edges(all_headings_and_links: dict):
    edges = set()
    for eachfile, heading_and_links in all_headings_and_links.items():
        for link in heading_and_links["links"]:
            edge = tuple(
                    sorted(
                        [
                            heading_and_links["heading"], 
                            all_headings_and_links[link]["heading"]
                        ]
                    )
                )
            if len(set(edge)) == 2:
                edges.add(edge)
    return edges

def get_nodes(all_headings_and_links: dict):
    nodes = set()
    for eachfile, heading_and_links in all_headings_and_links.items():
        nodes.add(heading_and_links["heading"])
    return nodes
