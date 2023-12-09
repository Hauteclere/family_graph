import unittest
from graph_builder import src

class MockDirectory(src.GraphedDirectory):
    def __init__(self):
        pass

class MockFile(src.GraphedFile):
    def __init__(self):
        pass

class TestGetAbsolutePath(unittest.TestCase):
    def test_null_string_path_returns_none(self):

        mock_file = MockFile()
        mock_file.p_path = "/"

        self.assertIsNone(mock_file.get_absolute_path(""))

#     def test_absolute_path_input(self):
#         absolute_path = "/home/olive/example.md"
#         parent = Path("/some/other/location")

#         self.assertEqual(
#             src.get_absolute_path(absolute_path, parent),
#             absolute_path
#         )

#     def test_normal_case(self):
#         relative_path = "./example.md"
#         parent = Path("/home/olive/files")

#         self.assertEqual(
#             src.get_absolute_path(relative_path, parent),
#             Path("/home/olive/files/example.md")
#         )

#     def test_anchor_links_truncated(self):
#         anchor_path = "./example.md#myanchor"
#         parent = Path("/home/olive/files")

#         self.assertEqual(
#             src.get_absolute_path(anchor_path, parent),
#             Path("/home/olive/files/example.md")
#         )

#     # Need more probably, better check

# class TestGetNodes(unittest.TestCase):
#     def test_duplicate_headings(self):
#         all_headings_and_links = {
#             "1.md": {
#                 "heading": "Same Heading",
#                 "links": []
#             },
#             "2.md": {
#                 "heading": "Same Heading",
#                 "links": []
#             }
#         }

#         with self.assertRaises(ValueError):
#             src.get_nodes(all_headings_and_links)