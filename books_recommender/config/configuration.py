"""
Configuration Manager Module

This module provides the `AppConfiguration` class, which is responsible for loading,
managing, and providing access to the application's configuration settings. It reads from
a YAML file and makes the configurations available as structured data classes (entities).
This centralization of configuration management makes the application more modular and
easier to maintain.
"""
import os, sys
from books_recommender.constant import *
from books_recommender.utils.util import read_yaml_file
from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelRecommendationConfig


class AppConfiguration:
    """
    The core configuration manager class. It loads all configuration from the main
    config file and provides getter methods to access them as typed data classes.
    """

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        """
        Initializes the AppConfiguration manager.

        Args:
            config_file_path (str): The path to the main YAML configuration file.
                                    Defaults to the path specified in the constants.
        
        Raises:
            AppException: If there is an error reading or parsing the config file.
        """
        try:
            # Load the main configuration file
            self.config_info = read_yaml_file(file_path=config_file_path)
            
            # Extract top-level configuration sections
            self.artifacts_config = self.config_info['artifacts_config']
            self.data_ingestion_config = self.config_info['data_ingestion_config']
            self.data_validation_config = self.config_info['data_validation_config']
            self.data_transformation_config = self.config_info['data_transformation_config']
            self.model_trainer_config = self.config_info['model_trainer_config']
            
            # Define common artifact directories for easy access
            self.artifacts_dir = self.artifacts_config['artifacts_dir']
            self.dataset_dir = os.path.join(self.artifacts_dir, self.data_ingestion_config['dataset_dir'])
            self.serialized_objects_dir = os.path.join(self.artifacts_dir, self.data_validation_config['serialized_objects_dir'])
            self.trained_model_dir = os.path.join(self.artifacts_dir, self.model_trainer_config['trained_model_dir'])

        except Exception as e:
            raise AppException(e, sys) from e
        

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Constructs and returns the data ingestion configuration.

        This method assembles the necessary paths for data ingestion based on the
        base artifact directories and the specific settings in the config file.

        Returns:
            DataIngestionConfig: A data class containing all settings for data ingestion.
        """
        try:
            # Construct full paths for raw and ingested data directories
            ingested_data_dir = os.path.join(self.dataset_dir, self.data_ingestion_config['ingested_dir'])
            raw_data_dir = os.path.join(self.dataset_dir, self.data_ingestion_config['raw_data_dir'])

            # Populate the data class
            response = DataIngestionConfig(
                dataset_download_url=self.data_ingestion_config['dataset_download_url'],
                raw_data_dir=raw_data_dir,
                ingested_dir=ingested_data_dir
            )

            logging.info(f"Data ingestion config: {response}")
            return response
        except Exception as e:
            raise AppException(e, sys) from e
        
    def get_validation_config(self) -> DataValidationConfig:
        """
        Constructs and returns the data validation configuration.

        This method assembles paths to the raw CSV files and the directories for
        cleaned data and serialized objects.

        Returns:
            DataValidationConfig: A data class containing all settings for data validation.
        """
        try:
            # Construct full paths for input CSV files and output directories
            books_csv_file_dir = os.path.join(self.dataset_dir, self.data_ingestion_config['ingested_dir'], self.data_validation_config['books_csv_file'])
            ratings_csv_file_dir = os.path.join(self.dataset_dir, self.data_ingestion_config['ingested_dir'], self.data_validation_config['ratings_csv_file'])
            clean_data_path = os.path.join(self.dataset_dir, self.data_validation_config['clean_data_dir'])

            # Populate the data class
            response = DataValidationConfig(
                clean_data_dir=clean_data_path,
                books_csv_file=books_csv_file_dir,
                ratings_csv_file=ratings_csv_file_dir,
                serialized_objects_dir=self.serialized_objects_dir
            )

            logging.info(f"Data validation config: {response}")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Constructs and returns the data transformation configuration.

        Returns:
            DataTransformationConfig: A data class for data transformation settings.
        """
        try:
            # Construct paths for the source clean data and the output transformed data directory
            clean_data_file_path = os.path.join(self.dataset_dir, self.data_validation_config['clean_data_dir'], 'clean_data.csv')
            transformed_data_dir = os.path.join(self.dataset_dir, self.data_transformation_config['transformed_data_dir'])

            response = DataTransformationConfig(
                clean_data_file_path=clean_data_file_path,
                transformed_data_dir=transformed_data_dir
            )

            logging.info(f"Data Transformation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """
        Constructs and returns the model trainer configuration.

        Returns:
            ModelTrainerConfig: A data class for model training settings.
        """
        try:
            # Construct the path to the transformed data file needed for training
            transformed_data_file = self.data_transformation_config['transformed_data_file_name']
            transformed_data_file_dir = os.path.join(self.dataset_dir, self.data_transformation_config['transformed_data_dir'], transformed_data_file)
            
            response = ModelTrainerConfig(
                transformed_data_file_dir=transformed_data_file_dir,
                trained_model_dir=self.trained_model_dir,
                trained_model_name=self.model_trainer_config['trained_model_name']
            )

            logging.info(f"Model Trainer Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    def get_recommendation_config(self) -> ModelRecommendationConfig:
        """
        Constructs and returns the configuration needed for the recommendation engine.
        This includes paths to all the serialized objects (final ratings, pivot table, model).

        Returns:
            ModelRecommendationConfig: A data class containing paths to necessary artifacts.
        """
        try:
            # Get the names of the serialized object files from the config
            book_names_file = self.data_validation_config['book_names_file_name']
            book_pivot_file = self.data_validation_config['book_pivot_table_file_name']
            final_rating_file = self.data_validation_config['final_rating_file_name']
            
            # Construct full paths to the serialized objects
            book_name_serialized_objects = os.path.join(self.serialized_objects_dir, book_names_file)
            book_pivot_serialized_objects = os.path.join(self.serialized_objects_dir, book_pivot_file)
            final_rating_serialized_objects = os.path.join(self.serialized_objects_dir, final_rating_file)

            # Construct the full path to the trained model
            trained_model_path = os.path.join(self.trained_model_dir, self.model_trainer_config['trained_model_name'])
          
            response = ModelRecommendationConfig(
                book_name_serialized_objects=book_name_serialized_objects,
                book_pivot_serialized_objects=book_pivot_serialized_objects,
                final_rating_serialized_objects=final_rating_serialized_objects,
                trained_model_path=trained_model_path
            )

            logging.info(f"Model Recommendation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e