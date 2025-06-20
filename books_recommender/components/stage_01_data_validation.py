import os
import sys
import pandas as pd
from books_recommender.logger.log import logging
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException

class DataValidation:
    def __init__(self, app_config=AppConfiguration()):
        try:
            self.data_validation_config = app_config.get_validation_config()
            self.data_ingestion_config = app_config.get_data_ingestion_config()
            self.expected_ratings_schema = {
                "User-ID": "int64",
                "ISBN": "object",
                "Book-Rating": "int64"
            }
            self.expected_books_schema = {
                "ISBN": "object",
                "Book-Title": "object",
                "Book-Author": "object",
                "Year-Of-Publication": "object",
                "Publisher": "object",
                "Image-URL-S": "object",
                "Image-URL-M": "object",
                "Image-URL-L": "object"
            }
        except Exception as e:
            raise AppException(e, sys) from e

    def validate_schema(self, dataframe: pd.DataFrame, schema: dict) -> bool:
        """
        Validates the schema of a given DataFrame.
        """
        try:
            logging.info("Starting schema validation.")
            if not all(col in dataframe.columns for col in schema.keys()):
                logging.error("Schema validation failed: Missing columns.")
                return False
            
            for col, dtype in schema.items():
                if dataframe[col].dtype != dtype:
                    # Allow for flexible integer types
                    if "int" in dtype and "int" in str(dataframe[col].dtype):
                        continue
                    logging.error(f"Schema validation failed for column '{col}'. Expected type {dtype}, found {dataframe[col].dtype}.")
                    return False
            
            logging.info("Schema validation successful.")
            return True
        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_validation(self):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20}")
            
            # Read datasets
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1')
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1', low_memory=False)

            # Validate schemas
            is_ratings_schema_valid = self.validate_schema(ratings, self.expected_ratings_schema)
            is_books_schema_valid = self.validate_schema(books, self.expected_books_schema)

            if not is_ratings_schema_valid or not is_books_schema_valid:
                raise ValueError("Schema validation failed. Exiting.")

            # Create an empty clean_data.csv as a signal that validation passed
            # The actual data transformation will happen in the next stage.
            clean_data_dir = self.data_validation_config.clean_data_dir
            os.makedirs(clean_data_dir, exist_ok=True)
            placeholder_file_path = os.path.join(clean_data_dir, "validation_passed.flag")
            with open(placeholder_file_path, "w") as f:
                f.write("Validation passed.")

            logging.info(f"Schema validation passed. A placeholder has been created at {placeholder_file_path}")
            logging.info(f"{'='*20}Data Validation log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e

    