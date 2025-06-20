"""
Data Transformation Module

This module is responsible for the third stage of the ML pipeline: Data Transformation.
It takes the raw, validated data and performs all the necessary cleaning, preprocessing,
and feature engineering steps to prepare it for model training. This includes renaming
columns, filtering data to create a more robust dataset, merging data sources, and
creating the final pivot table that will be used as input for the recommendation model.
"""
import os, sys
import pandas as pd
import pickle
from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration

class DataTransformation:
    """
    Handles the cleaning, merging, and transformation of the data.
    """
    def __init__(self, app_config=AppConfiguration()):
        """
        Initializes the DataTransformation component.

        Args:
            app_config (AppConfiguration): The application configuration manager instance.
        """
        try:
            self.app_config = app_config
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config = app_config.get_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def transform_data(self) -> (pd.DataFrame, pd.DataFrame):
        """
        Performs the core data transformation process.

        This method loads the raw books and ratings data, and then applies a series
        of transformations:
        1. Selects relevant columns and renames them for clarity.
        2. Filters out users with fewer than 200 ratings to focus on active users.
        3. Merges the books and ratings data.
        4. Filters out books with fewer than 50 ratings to focus on popular books.
        5. Removes duplicate user-book ratings.
        6. Creates a user-item pivot table, with book titles as rows, user IDs as
           columns, and ratings as values.

        Returns:
            A tuple containing:
            - pd.DataFrame: The final, cleaned, and merged ratings DataFrame.
            - pd.DataFrame: The user-item pivot table.
        """
        try:
            logging.info("Starting data transformation: loading raw data.")
            # Load raw data
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1')
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1', dtype={'Year-Of-Publication': str}, low_memory=False)

            logging.info(f"Shape of raw ratings: {ratings.shape}, Shape of raw books: {books.shape}")

            # Preprocessing and cleaning: select columns and rename for consistency
            books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
            books.rename(columns={"Book-Title": 'title', 'Book-Author': 'author', "Year-Of-Publication": 'year', "Publisher": "publisher", "Image-URL-L": "image_url"}, inplace=True)
            ratings.rename(columns={"User-ID": 'user_id', 'Book-Rating': 'rating'}, inplace=True)

            # Filter to include only users who have rated more than 200 books
            x = ratings['user_id'].value_counts() > 200
            y = x[x].index
            ratings = ratings[ratings['user_id'].isin(y)]

            # Merge ratings and books data on ISBN
            ratings_with_books = ratings.merge(books, on='ISBN')
            
            # Filter to include only books that have received 50 or more ratings
            number_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
            number_rating.rename(columns={'rating': 'num_of_rating'}, inplace=True)
            final_rating = ratings_with_books.merge(number_rating, on='title')
            final_rating = final_rating[final_rating['num_of_rating'] >= 50]
            # Remove duplicate ratings for the same book by the same user
            final_rating.drop_duplicates(['user_id', 'title'], inplace=True)
            
            logging.info(f"Shape of the final cleaned and merged dataset: {final_rating.shape}")
            
            # Create the user-item pivot table for the collaborative filtering model
            book_pivot = final_rating.pivot_table(columns='user_id', index='title', values='rating')
            book_pivot.fillna(0, inplace=True)
            logging.info(f"Shape of the created pivot table: {book_pivot.shape}")

            return final_rating, book_pivot

        except Exception as e:
            raise AppException(e, sys) from e

    def save_artifacts(self, final_rating: pd.DataFrame, book_pivot: pd.DataFrame):
        """
        Saves the transformed data and serialized objects.

        This method saves several critical artifacts:
        - The transformed pivot table (for model training).
        - The final ratings DataFrame (for the web app).
        - The pivot table (for the web app).
        - The list of book names (for the web app's dropdown).

        Args:
            final_rating (pd.DataFrame): The cleaned and merged ratings data.
            book_pivot (pd.DataFrame): The user-item pivot table.
        """
        try:
            logging.info("Saving transformation artifacts.")
            # Get file paths from config for clarity
            conf = self.app_config.data_transformation_config
            transformed_data_dir = self.data_transformation_config.transformed_data_dir
            transformed_data_file = os.path.join(transformed_data_dir, conf['transformed_data_file_name'])
            
            val_conf = self.app_config.data_validation_config
            serialized_objects_dir = self.data_validation_config.serialized_objects_dir
            final_rating_path = os.path.join(serialized_objects_dir, val_conf['final_rating_file_name'])
            book_pivot_path = os.path.join(serialized_objects_dir, val_conf['book_pivot_table_file_name'])
            book_names_path = os.path.join(serialized_objects_dir, val_conf['book_names_file_name'])

            # Ensure output directories exist
            os.makedirs(transformed_data_dir, exist_ok=True)
            os.makedirs(serialized_objects_dir, exist_ok=True)
            
            # Save all artifacts using pickle
            book_pivot.to_pickle(transformed_data_file)
            pickle.dump(final_rating, open(final_rating_path, 'wb'))
            pickle.dump(book_pivot, open(book_pivot_path, 'wb'))
            pickle.dump(book_pivot.index, open(book_names_path, 'wb'))

            logging.info(f"Saved transformed data to: {transformed_data_file}")
            logging.info(f"Saved serialized objects to directory: {serialized_objects_dir}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_transformation(self):
        """
        Orchestrates the entire data transformation process.

        This is the main entry point for the data transformation stage. It calls the
        methods to transform the data and save the resulting artifacts.
        """
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20}")
            final_rating, book_pivot = self.transform_data()
            self.save_artifacts(final_rating, book_pivot)
            logging.info(f"{'='*20}Data Transformation log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e
        
