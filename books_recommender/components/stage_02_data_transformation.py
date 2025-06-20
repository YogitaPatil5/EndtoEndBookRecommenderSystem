import os, sys
import pandas as pd
import pickle
from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration

class DataTransformation:
    def __init__(self, app_config=AppConfiguration()):
        """
        This method is used to initialize the DataTransformation class.
        It takes a single parameter:
        app_config: The configuration object.
        It returns:
        None
        """
        try:
            self.app_config = app_config
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config = app_config.get_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def transform_data(self):
        """
        This method is used to transform the data.
        It takes a single parameter:
        None
        It returns:
        final_rating: The final cleaned and merged dataset.
        book_pivot: The pivot table created from the final dataset.
        """
        try:
            logging.info("Starting data transformation: loading raw data.")
            # Load raw data
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1')
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1', dtype={'Year-Of-Publication': str}, low_memory=False)

            logging.info(f"Shape of raw ratings: {ratings.shape}, Shape of raw books: {books.shape}")

            # Preprocessing and cleaning
            books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
            books.rename(columns={"Book-Title": 'title', 'Book-Author': 'author', "Year-Of-Publication": 'year', "Publisher": "publisher", "Image-URL-L": "image_url"}, inplace=True)
            ratings.rename(columns={"User-ID": 'user_id', 'Book-Rating': 'rating'}, inplace=True)

            # Filter users who have rated at least 200 books
            x = ratings['user_id'].value_counts() > 200
            y = x[x].index
            ratings = ratings[ratings['user_id'].isin(y)]

            # Merge dataframes
            ratings_with_books = ratings.merge(books, on='ISBN')
            
            # Filter books with at least 50 ratings
            number_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
            number_rating.rename(columns={'rating': 'num_of_rating'}, inplace=True)
            final_rating = ratings_with_books.merge(number_rating, on='title')
            final_rating = final_rating[final_rating['num_of_rating'] >= 50]
            final_rating.drop_duplicates(['user_id', 'title'], inplace=True)
            
            logging.info(f"Shape of the final cleaned and merged dataset: {final_rating.shape}")
            
            # Create pivot table
            book_pivot = final_rating.pivot_table(columns='user_id', index='title', values='rating')
            book_pivot.fillna(0, inplace=True)
            logging.info(f"Shape of the created pivot table: {book_pivot.shape}")

            return final_rating, book_pivot

        except Exception as e:
            raise AppException(e, sys) from e

    def save_artifacts(self, final_rating, book_pivot):
        """
        This method is used to save the transformation artifacts.
        It takes two parameters:
        final_rating: The final cleaned and merged dataset.
        book_pivot: The pivot table created from the final dataset.
        It returns:
        None
        """
        try:
            logging.info("Saving transformation artifacts.")
            # Get file paths from config
            conf = self.app_config.data_transformation_config
            transformed_data_dir = self.data_transformation_config.transformed_data_dir
            transformed_data_file = os.path.join(transformed_data_dir, conf['transformed_data_file_name'])
            
            val_conf = self.app_config.data_validation_config
            serialized_objects_dir = self.data_validation_config.serialized_objects_dir
            final_rating_path = os.path.join(serialized_objects_dir, val_conf['final_rating_file_name'])
            book_pivot_path = os.path.join(serialized_objects_dir, val_conf['book_pivot_table_file_name'])
            book_names_path = os.path.join(serialized_objects_dir, val_conf['book_names_file_name'])

            # Create directories
            os.makedirs(transformed_data_dir, exist_ok=True)
            os.makedirs(serialized_objects_dir, exist_ok=True)
            
            # Save artifacts
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
        This method is used to initiate the data transformation.
        It takes a single parameter:
        None
        It returns:
        None
        """
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20}")
            final_rating, book_pivot = self.transform_data()
            self.save_artifacts(final_rating, book_pivot)
            logging.info(f"{'='*20}Data Transformation log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e
        
