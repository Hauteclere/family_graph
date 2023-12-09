from pathlib import Path, PosixPath
import markdown
import lxml.html

class GraphBuilderError(ValueError):
    def __init__(self, message):
        self.message = message
        super().__init__()

class DuplicateHeadingsError(GraphBuilderError):
    pass

class GraphedDirectory():
    def __init__(self, path_string: str) -> None:
        self.p_path = Path(path_string)
        self.files = {
            (self.p_path.parent.resolve() / str(eachpath)).resolve(): GraphedFile(
                self,
                eachpath
            ) for eachpath in self.markdown_file_addresses
        }

    @property
    def markdown_file_addresses(self) -> set:
        return {
            eachpath for eachpath in self.p_path.rglob(
                '*.md'
            ) 
        }
    
    @property
    def graph_details(self):
        nodes = set()

        for path, file in self.files.items():
            heading = file.heading
            if heading is None:
                continue
            if heading in nodes:
                bad_files = [
                    str(badpath) for badpath, bad_file in self.files.items() if bad_file.heading == file.heading
                ]
                message = f"Multiple pages have the same heading: {' and '.join(bad_files)}."
                
                raise DuplicateHeadingsError(message)
            nodes.add(heading)
        
        return {
            "nodes": nodes,
            "edges": {
                (
                    file.heading, 
                    self.files[link].heading
                ) for file in self.files.values() for link in file.links if link in self.files.keys()
            }
        }

    
class GraphedFile():
    def __init__(self, graphed_dir: GraphedDirectory, path: PosixPath) -> None:
        self.path = path

        with open(self.path) as file:
            self.graphed_dir = graphed_dir
            self.doctree = lxml.html.fromstring(markdown.markdown(file.read()))
    
    @property
    def heading(self) -> str:
        headings = self.doctree.xpath('//h1')
        if not headings:
            print(f"\t...WARNING: file at {self.path.resolve()} is malformed - no heading. \n\t\tThis file will not be added to the graph.")
            return None
        return headings[0].text
    
    @property
    def links(self) -> set:
        return set(
            map(
                self.get_absolute_path,
                (
                    eachlink.get('href') for eachlink in self.doctree.xpath('//a')
                )
            )
        )
    
    def get_absolute_path(self, somepath: str) -> Path:
        if not isinstance(somepath, str) or not len(somepath):
            return None
        if somepath[0] == "/":
            return Path(somepath)
        return (self.path.parent.resolve() / somepath.split('#')[0]).resolve()
        


    