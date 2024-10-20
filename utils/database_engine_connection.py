"""
This class is built to connect with DB engine
"""
from sqlalchemy import create_engine, URL
from utils.logger import setup_logging, get_logger
from utils.constants import C

# Setup logging
setup_logging()

# Get a logger for this module
logger = get_logger(__name__)

class DatabaseEngineConnection:
    def __init__(self):
        pass

    # PostgreSQL connection string
    def ingest_data(self, table_name, data):
        """
        Creates a SQLAlchemy engine to connect to PostgreSQL.
        """
        try:
            engine = create_engine(
                f"postgresql://{C.USER}:{C.PASSWORD}@{C.HOST}:{C.PORT}/{C.DBNAME}"
            )
            logger.info(f"Connected to PostgreSQL.")
            data.to_sql(table_name, engine, if_exists='replace', index=False)
            logger.info(f"Data ingestion successful for {table_name}.")
        except Exception as e:
            logger.error(f"Failed to ingest data into table {table_name}: {e}")
            raise

