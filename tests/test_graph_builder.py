import unittest
from graph_builder import src
from pathlib import Path

class TestGetAbsolutePath(unittest.TestCase):
    def test_null_string_path_returns_none(self):
        null_path = ""
        parent = Path("/")

        self.assertIsNone(src.get_absolute_path(null_path, parent))

    def test_absolute_path_input(self):
        absolute_path = "/home/olive/example.md"
        parent = Path("/some/other/location")

        self.assertEqual(
            src.get_absolute_path(absolute_path, parent),
            absolute_path
        )

    def test_normal_case(self):
        relative_path = "./example.md"
        parent = Path("/home/olive/files")

        self.assertEqual(
            src.get_absolute_path(relative_path, parent),
            Path("/home/olive/files/example.md")
        )

    def test_anchor_links_truncated(self):
        anchor_path = "./example.md#myanchor"
        parent = Path("/home/olive/files")

        self.assertEqual(
            src.get_absolute_path(anchor_path, parent),
            Path("/home/olive/files/example.md")
        )