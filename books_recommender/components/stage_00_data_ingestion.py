"""
Data Ingestion Module

This module is responsible for the first stage of the ML pipeline: Data Ingestion.
It handles downloading the raw dataset from a specified URL and extracting it.
The process is designed to be idempotent; it will not re-download data if it
already exists, making it efficient for repeated pipeline runs.
"""
import os
import sys
from six.moves import urllib
import zipfile
from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration


class DataIngestion:
    """
    Manages the downloading and extraction of the dataset.
    """

    def __init__(self, app_config=AppConfiguration()):
        """
        Initializes the DataIngestion component.

        Args:
            app_config (AppConfiguration): The application configuration manager instance.
        """
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20} ")
            self.data_ingestion_config = app_config.get_data_ingestion_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def download_data(self) -> str:
        """
        Fetches the dataset from the configured URL if it doesn't already exist locally.

        The method checks for the existence of the zip file in the raw data directory.
        If the file is not found, it downloads it from the URL specified in the
        configuration.

        Returns:
            str: The local file path to the downloaded zip file.
        """
        try:
            dataset_url = self.data_ingestion_config.dataset_download_url
            zip_download_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)

            # Download the file only if it does not exist
            if not os.path.exists(zip_file_path):
                logging.info(f"Downloading data from {dataset_url} into file {zip_file_path}")
                urllib.request.urlretrieve(dataset_url, zip_file_path)
                logging.info(f"Downloaded data successfully into file: {zip_file_path}")
            else:
                logging.info(f"File {zip_file_path} already exists. Skipping download.")

            return zip_file_path

        except Exception as e:
            raise AppException(e, sys) from e

    def extract_zip_file(self, zip_file_path: str):
        """
        Extracts the contents of a zip file to the ingested data directory.

        Args:
            zip_file_path (str): The path to the zip file to be extracted.
        """
        try:
            ingested_dir = self.data_ingestion_config.ingested_dir
            os.makedirs(ingested_dir, exist_ok=True)
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {ingested_dir}")
            
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(ingested_dir)
                logging.info(f"Extraction complete. Files extracted: {zip_ref.namelist()}")
        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_ingestion(self):
        """
        Orchestrates the data ingestion process: downloading and extracting.

        This is the main entry point for the data ingestion stage.
        """
        try:
            zip_file_path = self.download_data()
            self.extract_zip_file(zip_file_path=zip_file_path)
            logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e