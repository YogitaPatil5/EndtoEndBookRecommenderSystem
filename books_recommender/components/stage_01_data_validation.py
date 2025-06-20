"""
Data Validation Module

This module is responsible for the second stage of the ML pipeline: Data Validation.
It ensures that the raw data ingested in the previous stage conforms to a predefined
schema. This includes checking for the presence of required columns and verifying their
data types. This step is crucial for maintaining data quality and preventing errors
in downstream processing.
"""
import os
import sys
import pandas as pd
from books_recommender.logger.log import logging
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException

class DataValidation:
    """
    Performs schema validation on the raw datasets.
    """
    def __init__(self, app_config=AppConfiguration()):
        """
        Initializes the DataValidation component.

        It sets up the configuration and defines the expected schemas for the
        ratings and books datasets.

        Args:
            app_config (AppConfiguration): The application configuration manager instance.
        """
        try:
            self.data_validation_config = app_config.get_validation_config()
            self.data_ingestion_config = app_config.get_data_ingestion_config()
            
            # Define the expected schema for the ratings data
            self.expected_ratings_schema = {
                "User-ID": "int64",
                "ISBN": "object",
                "Book-Rating": "int64"
            }
            # Define the expected schema for the books data
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
        Validates the schema of a given DataFrame against an expected schema.

        It checks for two things:
        1. All expected columns are present in the DataFrame.
        2. The data type of each column matches the expected data type.

        Args:
            dataframe (pd.DataFrame): The DataFrame to validate.
            schema (dict): A dictionary representing the expected schema, where keys
                           are column names and values are expected data types.

        Returns:
            bool: True if the schema is valid, False otherwise.
        """
        try:
            logging.info("Starting schema validation.")
            # Check for missing columns
            if not all(col in dataframe.columns for col in schema.keys()):
                logging.error("Schema validation failed: Missing columns.")
                return False
            
            # Check for incorrect data types
            for col, dtype in schema.items():
                if dataframe[col].dtype != dtype:
                    # Allow for flexible integer types (e.g., int32 vs int64)
                    if "int" in dtype and "int" in str(dataframe[col].dtype):
                        continue
                    logging.error(f"Schema validation failed for column '{col}'. Expected type {dtype}, found {dataframe[col].dtype}.")
                    return False
            
            logging.info("Schema validation successful.")
            return True
        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_validation(self):
        """
        Orchestrates the data validation process.

        It reads the raw datasets, validates their schemas, and if successful,
        creates a flag file to signal that validation has passed, allowing the
        pipeline to proceed to the next stage.
        """
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20}")
            
            # Read raw datasets
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1')
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1', low_memory=False)

            # Validate schemas of both dataframes
            is_ratings_schema_valid = self.validate_schema(ratings, self.expected_ratings_schema)
            is_books_schema_valid = self.validate_schema(books, self.expected_books_schema)

            # If either schema is invalid, raise an error
            if not is_ratings_schema_valid or not is_books_schema_valid:
                raise ValueError("Schema validation failed. Exiting pipeline.")

            # Create a flag file to indicate successful validation.
            # This is a good practice in production pipelines to ensure a stage
            # has completed successfully before the next one begins.
            clean_data_dir = self.data_validation_config.clean_data_dir
            os.makedirs(clean_data_dir, exist_ok=True)
            placeholder_file_path = os.path.join(clean_data_dir, "validation_passed.flag")
            with open(placeholder_file_path, "w") as f:
                f.write("Validation passed.")

            logging.info(f"Schema validation successful. Flag file created at: {placeholder_file_path}")
            logging.info(f"{'='*20}Data Validation log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e

    