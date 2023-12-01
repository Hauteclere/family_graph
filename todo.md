# To Do

## Tests
| Condition                                   | Result                                                         | Written |
| ------------------------------------------- | -------------------------------------------------------------- | ------- |
| Links to anchors within documents exist     | edges still drawn between relevant docs                        |         |
| Docs exist within subdirectories            | edges still drawn to relevant docs                             |         |
| Docs link to files outside target directory | edges are not drawn outside target dir                         |         |
| docs link to files that do not exist        | edges are not drawn to files that do not exist                 |         |
| docs are missing headings                   | edges are not drawn to docs missing headings (warning printed) |         |
| docs link trivially (i.e. to themselves)    | trivial edges are not drawn                                    |         |
| docs are unlinked                           | nodes are still drawn                                          |         |
| what happens when a link has an empty path |                                                                |         |

## Functionality
- [ ] apply type enforcement and better hinting
- [ ] autogenerate locations of nodes in graph -> https://stackoverflow.com/questions/31415907/get-node-position-and-length-of-edge
- [ ] get graph as element instead of full doc
- [ ] add labels to graph
- [ ] set each node's link to a separate value