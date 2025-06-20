from books_recommender.components.stage_00_data_ingestion import DataIngestion
from books_recommender.exception.exception_handler import AppException
import sys
from books_recommender.components.stage_01_data_validation import DataValidation
from books_recommender.components.stage_02_data_transformation import DataTransformation
from books_recommender.components.stage_03_model_trainer import ModelTrainer

class TrainingPipeline:
    def __init__(self):
        """
        This method is used to initialize the TrainingPipeline class.
        It takes a single parameter:
        None
        It returns:
        None
        """
        try:
            self.data_ingestion = DataIngestion()
            self.data_validation = DataValidation()
            self.data_transformation = DataTransformation()
            self.model_trainer = ModelTrainer()
        except Exception as e:
            raise AppException(e, sys) from e
    
    def start_training_pipeline(self):
        """
        This method is used to start the training pipeline.
        It takes a single parameter:
        None
        It returns:
        None
        """
        try:
            self.data_ingestion.initiate_data_ingestion()
            self.data_validation.initiate_data_validation()
            self.data_transformation.initiate_data_transformation()
            self.model_trainer.initiate_model_trainer()
        except Exception as e:
            raise AppException(e, sys) from e