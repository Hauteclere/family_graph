import unittest
from graph_builder import src
from pathlib import Path
import markdown
import lxml.html
import io
import contextlib
from unittest.mock import patch

class MockDirectory(src.GraphedDirectory):
    def __init__(self):
        pass

class MockFile1(src.GraphedFile):
    def __init__(self):
        pass

class MockFile2(src.GraphedFile):
    def __init__(self, headingval=None, linksval=[]):
        self.headingval = headingval
        self.linksval = linksval

    @property
    def heading(self):
        if self.headingval is None:
            raise src.NoHeadingError("ERROR RAISED SUCCESSFULLY")
        return self.headingval
    
    @property
    def links(self):
        return self.linksval
    
class TestGraphedFile(unittest.TestCase):
    def test_null_string_path_returns_none(self):
        mock_file = MockFile1()
        mock_file.path = Path("/home/oliver/graphdocs/")
        self.assertIsNone(mock_file.get_absolute_path(""))

    def test_absolute_path_input(self):
        # Tests the case when a link in a document is an absolute path rather than a relative one.
        # get_absolute_path should just return its input as a path
        mock_file = MockFile1()
        mock_file.path = Path("/home/oliver/graphdocs/myfile.md")
        absolute_path_string = "/home/olive/example.md"
        absolute_path = Path(absolute_path_string)
        self.assertEqual(
            mock_file.get_absolute_path(absolute_path_string),
            absolute_path
        )
        
    def test_normal_case(self):
        mock_file = MockFile1()
        mock_file.path = Path("/home/oliver/graphdocs/myfile.md")
        relative_path = "./example.md"
        self.assertEqual(
            mock_file.get_absolute_path(relative_path),
            Path("/home/oliver/graphdocs/example.md")
        )

    def test_anchor_links_truncated(self):
        anchor_path = "./example.md#myanchor"
        mock_file = MockFile1()
        mock_file.path = Path("/home/oliver/graphdocs/myfile.md")

        self.assertEqual(
            mock_file.get_absolute_path(anchor_path),
            Path("/home/oliver/graphdocs/example.md")
        )

    def test_heading(self):
        mock_file = MockFile1()
        mock_file.doctree = lxml.html.fromstring(markdown.markdown("# Hello"))
        self.assertEqual("Hello", mock_file.heading)

    def test_no_heading(self):
        mock_file = MockFile1()
        mock_file.doctree = lxml.html.fromstring(markdown.markdown("## Hello"))
        mock_file.path = Path("/home/oliver/graphdocs/myfile.md")
        
        with self.assertRaises(src.NoHeadingError):
            mock_file.heading   

    def test_links(self):
        mock_file = MockFile1()
        mock_file.doctree = lxml.html.fromstring(markdown.markdown("[](./test_file_1.md)\n[](./test_file_1.md)"))
        mock_file.path = Path("/home/oliver/graphdocs/myfile.md")
        for link in mock_file.links:
            self.assertIn(
                link,
                {
                    Path("/home/oliver/graphdocs/test_file_1.md"),
                    Path("/home/oliver/graphdocs/test_file_2.md")
                }
            )

class TestGraphedDirectory(unittest.TestCase):
    # Doesn't test what happens if non-markdown files are present...
    # Seems pretty much a no-brainer though - that's how rglob works.
    def test_file_addresses(self):
        with patch.object(
            Path, 
            'rglob', 
            return_value=[
                "testfile.md", 
                "otherfiles/othertestfile.md"
            ]
        ) as mock_method:
            mydir = MockDirectory()
            mydir.p_path=Path("/some/test/path/")
            for eachaddress in [
                "testfile.md", 
                "otherfiles/othertestfile.md"
            ]:
                self.assertIn(
                    eachaddress,
                    mydir.markdown_file_addresses
                )
    
    # Doesn't test what happens if non-markdown files are present...
    # Seems pretty much a no-brainer though - that's how rglob works.
    def test_no_addresses(self):
        with patch.object(
            Path, 
            'rglob', 
            return_value=[
            ]
        ) as mock_method:
            mydir = MockDirectory()
            mydir.p_path=Path("/some/test/path/")
            for eachaddress in [
                "testfile.md", 
                "otherfiles/othertestfile.md"
            ]:
                self.assertEqual(
                    0,
                    len(mydir.markdown_file_addresses)
                )

    def test_file_lacks_heading(self):
        mock_file1 = MockFile2("Normal Heading")
        mock_file2 = MockFile2()

        mock_file1.path = Path("1.md")
        mock_file2.path = Path("2.md")

        mock_directory = MockDirectory()
        mock_directory.files = {
            "1.md": mock_file1,
            "2.md": mock_file2
        }

        f = io.StringIO()
        caught_string = f"ERROR RAISED SUCCESSFULLY"

        with contextlib.redirect_stdout(f):    
            deets = mock_directory.graph_details
            self.assertEqual(deets["nodes"], {"Normal Heading"})
            self.assertEqual(len(deets["nodes"]), 1)
            self.assertEqual(len(deets["edges"]), 0)
        
        self.assertTrue(
            caught_string in f.getvalue()
        )

    def test_duplicate_headings(self):
        mock_file1 = MockFile2("Normal Heading")
        mock_file2 = MockFile2("Normal Heading")

        mock_file1.path = Path("1.md")
        mock_file2.path = Path("2.md")

        mock_directory = MockDirectory()
        mock_directory.files = {
            "1.md": mock_file1,
            "2.md": mock_file2
        }

        with self.assertRaises(src.DuplicateHeadingsError):
            mock_directory.graph_details

    def test_details_correct_in_normal_case(self):
        mock_file1 = MockFile2("file_1", ["2.md"])
        mock_file2 = MockFile2("file_2", ["3.md"])

        mock_file1.path = Path("1.md")
        mock_file2.path = Path("2.md")

        mock_directory = MockDirectory()
        mock_directory.files = {
            "1.md": mock_file1,
            "2.md": mock_file2
        }

        expected_result = {
            'nodes': {'file_2', 'file_1'}, 
            'edges': {
                ('file_1', 'file_2')
            }
        }

        self.assertEqual(
            expected_result, 
            mock_directory.graph_details
        )