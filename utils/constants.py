from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass(frozen=True)
class Constants:
    # buckets path
    SOURCE_BUCKET: str = "buckets/source"
    SUCCESS_BUCKET: str = "buckets/success"
    FAILED_BUCKET: str = "buckets/failed"
    PROCESSING_BUCKET: str = "buckets/processing"
    BASE_PATH: str = "/home/lanius/PythonProjects/Stream_Data_Engineering_Task"

    POSTGRES_TABLE = {
        "transactions.csv": "transactions",
        "users.csv": "users",
        "products.csv": "products",
    }

    # primary keys
    PK = {
        "transactions.csv": "transaction_id",
        "users.csv": "customer_id",
        "products.csv": "subscription_id",
    }

    # foreign keys
    FK = {
        "transactions.csv": ["customer_id", "subscription_id"],
    }

    # postgres server
    TYPE: str = "postgres"
    HOST: str = "localhost"
    USER: str = "postgres"
    PASSWORD: str = quote_plus("Pp@639493")
    PORT: str = "5432"
    DBNAME: str = "DWH"
    SCHEMA: str = "public"


C = Constants()
