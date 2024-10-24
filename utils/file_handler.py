import os
import shutil

from utils.constants import C
from utils.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


class FileHandler:
    def __init__(self):
        # filled for cloud to initiate (boto3)
        pass

    def get_contents(self, bucket):
        """
        Retrieves the contents of the bucket
        Args:
            bucket: bucket's name
        :return:
            str: contents of buckets
        """
        bucket = f"{C.BASE_PATH}/{bucket}"
        try:
            contents = os.listdir(bucket)
            logger.info(f"Contents of bucket '{bucket}': {contents}")
            return contents
        except FileNotFoundError:
            logger.error(f"Bucket '{bucket}' does not exist.")
            return None
        except Exception as e:
            logger.error(f"An error occurred while listing the contents of '{bucket}': {e}")
            return None

    def move_file(self, source_bucket, destination_bucket, file_name):
        """
        moves the file from source to destination bucket
        Args:
            source_bucket: source bucket
            destination_bucket: destination bucket
            file_name: file name to move
        :return:
            bool: True if move is successful
        """
        try:
            source_path = f"{C.BASE_PATH}/{source_bucket}/{file_name}"
            destination_path = f"{C.BASE_PATH}/{destination_bucket}/{file_name}"

            # Move the file
            shutil.move(source_path, destination_path)
            logger.info(f"Moved file '{file_name}' from '{source_bucket}' to '{destination_bucket}'")
            return True
        except FileNotFoundError:
            logger.error(f"File '{file_name}' or bucket does not exist.")
            return False
        except Exception as e:
            logger.error(f"Failed to move file '{file_name}': {e}")
            return False

    def check_bucket(self, bucket_path):
        """
        Check if bucket exists before moving
        Arg:
            bucket_name: bucket name
        :return:
            bool: True if the bucket exists, False otherwise
        """
        try:
            if os.path.isdir(bucket_path):
                logger.info(f"Bucket '{bucket_path}' exists.")
                return True
            else:
                logger.warning(f"Bucket '{bucket_path}' does not exist.")
                return False
        except Exception as e:
            logger.error(f"An error occurred while checking the bucket '{bucket_path}': {e}")
            return False

    def is_file_processed(self, file_name):
        """
        Checks if the file is in the processed folder
        Args:
            bucket_name: bucket name
            file_name: file name to be checked
        :return:
        """
        try:
            success_path = f"{C.BASE_PATH}/{C.SUCCESS_BUCKET}"
            file_success_path = f"{success_path}/{file_name}"

            if os.path.isfile(file_success_path):
                logger.info(f"File '{file_name}' has been processed and exists in '{C.SUCCESS_BUCKET}'")
                return True
            else:
                logger.warning(f"File '{file_name}' has not been processed yet.")
                return False
        except Exception as e:
            logger.error(f"An error occurred while checking if '{file_name}' is processed: {e}")
            return False

    def validate_bucket_and_file(self, bucket_name, file_name):
        """
        Validating if bucket exists and
        :return:
        """
        bucket_path = f"{C.BASE_PATH}/{bucket_name}"
        file_path = f"{bucket_path}/{file_name}"

        if not self.check_bucket(bucket_path):
            logger.error(f"Validation failed: Bucket '{bucket_name}' does not exist.")
            return False

        if not os.path.isfile(file_path):
            logger.warning(f"Validation failed: File '{file_name}' does not exist in bucket '{bucket_name}'.")
            return False

        if self.is_file_processed(file_name):
            logger.error(f"Validation failed: File '{file_name}' has already been processed.")
            raise ValueError(f"File '{file_name}' has already been processed.")

        logger.info(f"Bucket '{bucket_name}' and file '{file_name}' are valid for processing.")
        return True
