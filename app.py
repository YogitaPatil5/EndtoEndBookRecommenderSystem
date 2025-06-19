from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
import os,sys

# try:
#     logging.info("Starting the application")
#     a=1/0
# except Exception as e:
#     logging.info(e)
#     raise AppException(e, sys) from e