"""
Training Pipeline Module

This module defines the main training pipeline for the book recommender system.
It orchestrates the entire ML workflow by initializing and running each of the
pipeline's stages in the correct order:
1. Data Ingestion
2. Data Validation
3. Data Transformation
4. Model Training

This modular approach makes the pipeline easy to manage, debug, and extend.
"""
from books_recommender.components.stage_00_data_ingestion import DataIngestion
from books_recommender.exception.exception_handler import AppException
import sys
from books_recommender.components.stage_01_data_validation import DataValidation
from books_recommender.components.stage_02_data_transformation import DataTransformation
from books_recommender.components.stage_03_model_trainer import ModelTrainer

class TrainingPipeline:
    """
    Orchestrates the execution of the machine learning training pipeline.
    """
    def __init__(self):
        """
        Initializes the TrainingPipeline by creating instances of each pipeline stage.
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
        Executes the training pipeline by calling each stage in sequence.

        This method systematically runs the data ingestion, validation, transformation,
        and model training stages. If any stage fails, the pipeline will stop and
        the exception will be caught and logged by the custom exception handler.
        """
        try:
            # Stage 1: Data Ingestion
            self.data_ingestion.initiate_data_ingestion()
            
            # Stage 2: Data Validation
            self.data_validation.initiate_data_validation()
            
            # Stage 3: Data Transformation
            self.data_transformation.initiate_data_transformation()
            
            # Stage 4: Model Training
            self.model_trainer.initiate_model_trainer()
        except Exception as e:
            raise AppException(e, sys) from e