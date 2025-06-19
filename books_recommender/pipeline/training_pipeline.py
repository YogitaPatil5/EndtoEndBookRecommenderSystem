from books_recommender.components.stage_00_data_ingestion import DataIngestion
#from books_recommender.exception.exception_handler import AppException
#import sys

class TrainingPipeline:
    def __init__(self):
        """
        This method is used to initialize the TrainingPipeline class.
        It takes a single parameter:
        None
        It returns:
        None
        """
        #try:
        self.data_ingestion = DataIngestion()
        #except Exception as e:
         #   raise AppException(e, sys) from e
    
    def start_training_pipeline(self):
        """
        This method is used to start the training pipeline.
        It takes a single parameter:
        None
        It returns:
        None
        """
       # try:
        self.data_ingestion.initiate_data_ingestion()
        #except Exception as e:
         #   raise AppException(e, sys) from e