import unittest
from unittest.mock import patch, MagicMock
from utils.file_handler import FileHandler
from utils.constants import C
import os


class TestFileHandler(unittest.TestCase):

    @patch('utils.file_handler.os.listdir')
    @patch('utils.file_handler.logger')
    def test_get_contents_success(self, mock_logger, mock_listdir):
        # Arrange
        file_handler = FileHandler()
        mock_listdir.return_value = ['file1.csv', 'file2.csv']
        bucket = "test_bucket"

        # Act
        result = file_handler.get_contents(bucket)

        # Assert
        mock_listdir.assert_called_once_with(f"{C.BASE_PATH}/{bucket}")
        mock_logger.info.assert_called_with(f"Contents of bucket '{C.BASE_PATH}/{bucket}': ['file1.csv', 'file2.csv']")
        self.assertEqual(result, ['file1.csv', 'file2.csv'])


if __name__ == '__main__':
    unittest.main()
