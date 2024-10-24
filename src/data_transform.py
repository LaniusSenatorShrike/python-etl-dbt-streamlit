import pandas as pd

from utils.constants import C


class DataTransformer:
    def __init__(self):
        pass

    def read_csv(self, file_name):
        """
        Reads a CSV file into a pandas DataFrame.

        :param file_path: Path to the CSV file
        :return: DataFrame containing the CSV data
        """
        file_path = f"{C.BASE_PATH}/{C.PROCESSING_BUCKET}/{file_name}"
        return pd.read_csv(file_path)

    def clean_column_names(self, data):
        """
        Replaces spaces and () in column names with underscores and converts them to lowercase.

        :param data: Input data as a pandas DataFrame
        :return: DataFrame with cleaned column names
        """
        data.columns = data.columns.str.replace(" ", "_").str.replace("(", "").str.replace(")", "").str.lower()

        return data

    def standardize_date(self, data):
        """
        Automatically detects columns with date-like values and standardizes the formats.

        :param data: Input data as a pandas DataFrame
        :return: DataFrame with standardized date columns
        """
        for column in data.columns:
            if "date" in column.lower():  # Check if 'date' is in the column name (case-insensitive)
                try:
                    # Try to convert the column to datetime format
                    data[column] = pd.to_datetime(data[column], format="%m/%d/%y %H:%M", errors="raise")
                except (ValueError, TypeError):
                    # If conversion fails, skip the column and leave it unchanged
                    pass

        return data

    def handle_missing_and_duplicates(self, data):
        """
        Handles missing and duplicate records.

        - Fills missing values
        - Removes duplicate records

        :param data: Input data as a pandas DataFrame
        :return: Cleaned DataFrame
        """

        # Filling missing values with forward fill
        data = data.fillna("NULL")

        # Removing duplicate records
        data = data.drop_duplicates()

        return data

    def create_relational_schema(self, data, primary_key, foreign_keys):
        """
        Establishes primary and foreign keys in the DataFrame.

        :param data: Input data as a pandas DataFrame
        :param primary_key: Column to be set as the primary key
        :param foreign_keys: List of columns to be set as foreign keys
        :return: DataFrame with primary and foreign keys
        """
        # Set the primary key
        # drop = False is being used to avoid dropping column while indexing it.
        # if it's removed, the indexed column is not ingested bc it's an index and not a column anymore
        data.set_index(primary_key, drop=False, inplace=True)

        # Store the primary key and foreign keys in a dictionary in _metadata
        data._metadata = {"primary_key": primary_key, "foreign_keys": foreign_keys}

        return data

    def check_relational_schema(self, data):
        """
        Check the primary and foreign keys for the given DataFrame.

        :param data: Input data as a pandas DataFrame
        :return: Dictionary with primary key and foreign keys
        """
        # Retrieve the primary key and foreign keys from _metadata
        primary_key = data._metadata.get("primary_key", None)
        foreign_keys = data._metadata.get("foreign_keys", [])

        # Print or return the relational schema information
        schema_info = {"Primary Key": primary_key, "Foreign Keys": foreign_keys}

        return schema_info

    def calculate_total_spending_per_user(self, data, group_by_column, aggregation_column):
        """
        Calculates the total spending per user.
        """
        result = data.groupby(group_by_column)[aggregation_column].sum().reset_index()
        # Rename the columns for clarity
        result.columns = [group_by_column, "total_spending"]
        return result
