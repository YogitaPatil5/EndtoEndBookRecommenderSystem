import yaml
import sys
from books_recommender.exception.exception_handler import AppException


#Reading yaml file
def read_yaml_file(file_path:str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    Args:
        file_path (str): The path to the YAML file.
    Returns:
        dict: The contents of the YAML file as a dictionary.
    Raises:
        AppException: If the file is not found or there is an error reading the file.
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise AppException(e, sys) from e
    
