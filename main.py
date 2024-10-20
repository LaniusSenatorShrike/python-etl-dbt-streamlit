import logging
import re
from utils.constants import C
from utils.logger import get_logger, setup_logging
from utils.file_handler import FileHandler
from src.data_transform import DataTransformer

from utils.database_engine_connection import DatabaseEngineConnection

# Setup logging
setup_logging()

# Get a logger for this module
logger = get_logger(__name__)


def main():
    """
    main function to start data processing and ingestion
    """
    handler = FileHandler()
    transformer = DataTransformer()
    ingest_data = DatabaseEngineConnection().ingest_data

    logger.info("Checking source bucket contents")
    contents = handler.get_contents(C.SOURCE_BUCKET)

    for file in contents:
        filename = re.sub(r'\.csv$', '', file)
        try:
            logger.info(f"Bucket and file validation initiated for {file}")
            handler.validate_bucket_and_file(C.SOURCE_BUCKET, file)

            logger.info(f"Processing initiated for {file}")
            handler.move_file(C.SOURCE_BUCKET, C.PROCESSING_BUCKET, file)

            data = transformer.read_csv(file)
            data = transformer.clean_column_names(data)
            std_data = transformer.standardize_date(data)
            handled_std_data = transformer.handle_missing_and_duplicates(std_data)

            primary_key = C.PK.get(file)
            foreign_keys = C.FK.get(file, [])

            # if primary key dict is not empty
            if C.PK:
                logger.info(f"Applying relational schema for {file} with primary key {primary_key} and foreign keys {foreign_keys}")
                # Check and print the schema information with transformer.check_relational_schema
                handled_std_data_idx = transformer.create_relational_schema(handled_std_data, primary_key, foreign_keys)
            else:
                logger.info(f"No primary key found for {file}")
                handled_std_data_idx = handled_std_data

            # Calculate total spending per user (for transactions.csv)
            if filename == 'transactions':
                logger.info(f"Calculating total spending per user for {file}")
                total_spending_per_user = transformer.calculate_total_spending_per_user(handled_std_data_idx, 'customer_id', 'total')

                # Ingest total spending per user into a separate table
                spending_table_name = "total_spending_per_user"
                logger.info(f"Ingesting total spending per user into table: {spending_table_name}")
                ingest_data(spending_table_name, total_spending_per_user)

            # checking the connection
            logger.info(f"Ingesting data into table: {filename}")
            ingest_data(filename, handled_std_data_idx)

            handler.move_file(C.PROCESSING_BUCKET, C.SUCCESS_BUCKET, file)
            logger.info(f"Processing ended for {file}")

        except Exception as e:
            logger.error(f"File moved to failed bucket due to error: {e}")
            handler.move_file(C.PROCESSING_BUCKET, C.FAILED_BUCKET, file)

if __name__ == "__main__":
    main()

