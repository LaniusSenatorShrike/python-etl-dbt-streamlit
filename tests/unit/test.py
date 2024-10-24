import unittest
from unittest.mock import MagicMock, patch

from utils.constants import C
from utils.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):

    @patch("utils.file_handler.os.listdir")
    @patch("utils.file_handler.logger")
    def test_get_contents_success(self, mock_logger, mock_listdir):
        # Arrange
        file_handler = FileHandler()
        mock_listdir.return_value = ["file1.csv", "file2.csv"]
        bucket = "test_bucket"

        # Act
        result = file_handler.get_contents(bucket)

        # Assert
        mock_listdir.assert_called_once_with(f"{C.BASE_PATH}/{bucket}")
        mock_logger.info.assert_called_with(f"Contents of bucket '{C.BASE_PATH}/{bucket}': ['file1.csv', 'file2.csv']")
        self.assertEqual(result, ["file1.csv", "file2.csv"])

    @patch("utils.file_handler.os.listdir")
    @patch("utils.file_handler.logger")
    def test_get_contents_bucket_not_exist(self, mock_logger, mock_listdir):
        # Arrange
        file_handler = FileHandler()
        mock_listdir.side_effect = FileNotFoundError
        bucket = "non_existent_bucket"

        # Act
        result = file_handler.get_contents(bucket)

        # Assert
        mock_listdir.assert_called_once_with(f"{C.BASE_PATH}/{bucket}")
        mock_logger.error.assert_called_with(f"Bucket '{C.BASE_PATH}/{bucket}' does not exist.")
        self.assertIsNone(result)

    @patch("utils.file_handler.os.listdir")
    @patch("utils.file_handler.logger")
    def test_get_contents_unexpected_exception(self, mock_logger, mock_listdir):
        # Arrange
        file_handler = FileHandler()
        mock_listdir.side_effect = Exception("Unexpected Error")
        bucket = "test_bucket"

        # Act
        result = file_handler.get_contents(bucket)

        # Assert
        mock_listdir.assert_called_once_with(f"{C.BASE_PATH}/{bucket}")
        mock_logger.error.assert_called_with(
            f"An error occurred while listing the contents of '{C.BASE_PATH}/{bucket}': Unexpected Error"
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
