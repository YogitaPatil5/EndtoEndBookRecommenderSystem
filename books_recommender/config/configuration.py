import os, sys
from books_recommender.constant import *
from books_recommender.utils.util import read_yaml_file
from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelRecommendationConfig


class AppConfiguration:

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        """
        This method is used to initialize the AppConfiguration class.
        It takes a single parameter:
        config_file_path: The path to the configuration file.
        It returns:
        None
        """
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.artifacts_config = self.config_info['artifacts_config']
            self.data_ingestion_config = self.config_info['data_ingestion_config']
            self.data_validation_config = self.config_info['data_validation_config']
            self.data_transformation_config = self.config_info['data_transformation_config']
            self.model_trainer_config = self.config_info['model_trainer_config']
            
            # Define artifact directories
            self.artifacts_dir = self.artifacts_config['artifacts_dir']
            self.dataset_dir = os.path.join(self.artifacts_dir, self.data_ingestion_config['dataset_dir'])
            self.serialized_objects_dir = os.path.join(self.artifacts_dir, self.data_validation_config['serialized_objects_dir'])
            self.trained_model_dir = os.path.join(self.artifacts_dir, self.model_trainer_config['trained_model_dir'])

        except Exception as e:
            raise AppException(e, sys) from e
        

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        This method is used to get the data ingestion configuration.
        It returns:
        DataIngestionConfig: The data ingestion configuration.
        """
        try:
            ingested_data_dir = os.path.join(self.dataset_dir, self.data_ingestion_config['ingested_dir'])
            raw_data_dir = os.path.join(self.dataset_dir, self.data_ingestion_config['raw_data_dir'])

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
        This method is used to get the data validation configuration.
        It returns:
        DataValidationConfig: The data validation configuration.
        """
        try:
            books_csv_file_dir = os.path.join(self.dataset_dir, self.data_ingestion_config['ingested_dir'], self.data_validation_config['books_csv_file'])
            ratings_csv_file_dir = os.path.join(self.dataset_dir, self.data_ingestion_config['ingested_dir'], self.data_validation_config['ratings_csv_file'])
            clean_data_path = os.path.join(self.dataset_dir, self.data_validation_config['clean_data_dir'])

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
        This method is used to get the data transformation configuration.
        It returns:
        DataTransformationConfig: The data transformation configuration.
        """
        try:
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
        This method is used to get the model trainer configuration.
        It returns:
        ModelTrainerConfig: The model trainer configuration.
        """
        try:
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
        This method is used to get the recommendation configuration.
        It returns:
        ModelRecommendationConfig: The recommendation configuration.
        """
        try:
            book_names_file = self.data_validation_config['book_names_file_name']
            book_pivot_file = self.data_validation_config['book_pivot_table_file_name']
            final_rating_file = self.data_validation_config['final_rating_file_name']
            
            book_name_serialized_objects = os.path.join(self.serialized_objects_dir, book_names_file)
            book_pivot_serialized_objects = os.path.join(self.serialized_objects_dir, book_pivot_file)
            final_rating_serialized_objects = os.path.join(self.serialized_objects_dir, final_rating_file)

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