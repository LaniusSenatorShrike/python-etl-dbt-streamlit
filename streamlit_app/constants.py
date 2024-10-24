from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass(frozen=True)
class Constants:

    # postgres server
    TYPE: str = "postgres"
    HOST: str = "localhost"
    USER: str = "postgres"
    PASSWORD: str = "Pp@639493"
    PORT: str = "5432"
    DBNAME: str = "DWH"
    SCHEMA: str = "public"


C = Constants()
