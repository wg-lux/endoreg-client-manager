from django.test import TestCase
from unittest.mock import patch
from ..tasks import collect_data
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import shutil
import os
from django.test import TestCase
from ..utils import find_files

class CollectDataTest(TestCase):
    def setUp(self):
        self.dropoff_dir = Path(tempfile.mkdtemp())  # Use Path objects
        self.pseudo_dir = Path(tempfile.mkdtemp())
        self.test_files = [self.dropoff_dir / f"file{i}.txt" for i in range(3)]
        for file_path in self.test_files:
            with open(file_path, 'w') as f:
                f.write("Hello, world!")

    def tearDown(self):
        shutil.rmtree(self.dropoff_dir)
        shutil.rmtree(self.pseudo_dir)
                
    @patch('content_management.tasks.shutil.move')
    @patch('content_management.tasks.find_files')
    @patch('pathlib.Path.exists')
    def test_data_collection_task(self, mock_exists, mock_find_files, mock_move):
        mock_exists.return_value = True
        mock_find_files.return_value = self.test_files

        collect_data(self.dropoff_dir, self.pseudo_dir)

        # Check the calls to shutil.move
        expected_calls = [
            (str(mock_file), str(self.pseudo_dir / mock_file.name))
            for mock_file in self.test_files
        ]
        actual_calls = [(str(call[0][0]), str(call[0][1])) for call in mock_move.call_args_list]
        
        for expected_call in expected_calls:
            self.assertIn(expected_call, actual_calls, f"Expected move not found: {expected_call}")

        self.assertEqual(mock_move.call_count, 3, "Expected three files to be moved")
        
class TestFindFiles(TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = Path(tempfile.mkdtemp())
        # Create some files
        self.files = [
            self.test_dir / "test1.txt",
            self.test_dir / "test2.txt",
            self.test_dir / "example1.txt",
            self.test_dir / "example2.txt",
            self.test_dir / "archive.tar.gz"
        ]
        for file in self.files:
            file.touch()  # This creates the file

    def tearDown(self):
        # Remove the temporary directory and all files within it
        shutil.rmtree(self.test_dir)

    def test_find_no_files(self):
        patterns = ['*.docx']
        found_files = find_files(self.test_dir, patterns)
        self.assertEqual(len(found_files), 0)

    def test_find_single_file(self):
        patterns = ['*.tar.gz']
        found_files = find_files(self.test_dir, patterns)
        self.assertEqual(len(found_files), 1)
        self.assertIn(self.test_dir / "archive.tar.gz", found_files)

    def test_find_multiple_files(self):
        patterns = ['*.txt']
        found_files = find_files(self.test_dir, patterns)
        self.assertEqual(len(found_files), 4)

    def test_find_multiple_patterns(self):
        patterns = ['*.txt', '*.tar.gz']
        found_files = find_files(self.test_dir, patterns)
        self.assertEqual(len(found_files), 5)

    def test_empty_patterns(self):
        patterns = []
        found_files = find_files(self.test_dir, patterns)
        self.assertEqual(len(found_files), 0)

