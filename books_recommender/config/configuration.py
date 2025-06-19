import os, sys
from books_recommender.constant import *
from books_recommender.utils.util import read_yaml_file
from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.entity.config_entity import DataIngestionConfig



class AppConfiguration:

    def __init__(self, config_file_path:str=CONFIG_FILE_PATH):
        """
        This method is used to initialize the AppConfiguration class.
        It takes a single parameter:
        config_file_path: The path to the configuration file.
        It returns:
        None
        """
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e
        

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        This method is used to get the data ingestion configuration.
        It returns:
        DataIngestionConfig: The data ingestion configuration.
        """
        try:
            data_ingestion_config = self.config_info['data_ingestion_config']
            artifacts_dir = self.config_info['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']

            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'])
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['raw_data_dir'])

            response = DataIngestionConfig(
                dataset_download_url = data_ingestion_config['dataset_download_url'],
                raw_data_dir = raw_data_dir,
                ingested_dir = ingested_data_dir
            )

            logging.info(f"Data ingestion config: {response}")
            return response
        except Exception as e:
            raise AppException(e, sys) from e
        