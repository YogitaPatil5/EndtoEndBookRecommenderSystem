"""
Model Trainer Module

This module is responsible for the fourth stage of the ML pipeline: Model Training.
It takes the transformed data (the user-item pivot table) from the previous stage,
trains a K-Nearest Neighbors (KNN) model on it, and then saves the trained model
as a serialized object (pickle file) for later use in the recommendation engine.
"""
import os
import sys
import pickle
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from books_recommender.logger.log import logging
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException


class ModelTrainer:
    """
    Handles the training of the recommendation model and saving the artifact.
    """
    def __init__(self, app_config=AppConfiguration()):
        """
        Initializes the ModelTrainer component.

        Args:
            app_config (AppConfiguration): The application configuration manager instance.
        """
        try:
            self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def train(self):
        """
        Trains the KNN model and saves it.

        The process involves:
        1. Loading the user-item pivot table created during data transformation.
        2. Converting the pivot table into a sparse matrix for memory efficiency.
        3. Initializing a NearestNeighbors model with the algorithm specified in the config.
        4. Fitting the model to the sparse matrix.
        5. Saving the trained model object to a pickle file in the trained models artifact directory.
        """
        try:
            # Loading the transformed pivot table
            with open(self.model_trainer_config.transformed_data_file_dir, 'rb') as f:
                book_pivot = pickle.load(f)
            
            # Convert to a sparse matrix for efficient computation
            book_sparse = csr_matrix(book_pivot)
            logging.info(f"Loaded book_pivot and converted to sparse matrix with shape: {book_sparse.shape}")

            # Training the NearestNeighbors model
            algorithm = self.model_trainer_config.model_algorithm
            model = NearestNeighbors(algorithm=algorithm)
            logging.info(f"Training model with algorithm: '{algorithm}'")
            model.fit(book_sparse)
            logging.info("Model training completed successfully.")

            # Saving the trained model object
            os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
            file_name = os.path.join(self.model_trainer_config.trained_model_dir, self.model_trainer_config.trained_model_name)
            with open(file_name, 'wb') as f:
                pickle.dump(model, f)
            logging.info(f"Saved trained model to: {file_name}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_model_trainer(self):
        """
        Orchestrates the model training process.
        
        This is the main entry point for the model training stage.
        """
        try:
            logging.info(f"{'='*20}Model Trainer log started.{'='*20} ")
            self.train()
            logging.info(f"{'='*20}Model Trainer log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e
