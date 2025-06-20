from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
import os,sys

# try:
#     logging.info("Starting the application")
#     a=1/0
# except Exception as e:
#     logging.info(e)
#     raise AppException(e, sys) from e

import os, sys
import pickle
import pandas as pd
import numpy as np
import streamlit as st
from books_recommender.logger.log import logging
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException
from books_recommender.pipeline.training_pipeline import TrainingPipeline


class Recommendation:
    def __init__(self, app_config = AppConfiguration()):
        """
        This method is used to initialize the Recommendation class.
        It takes a single parameter:
        app_config: The configuration object.
        It returns:
        None
        """
        try:
            self.recommendation_config = app_config.get_recommendation_config()

        except Exception as e:
            raise AppException(e, sys) from e
        
    def fetch_poster(self, suggestion):
        """
        This method is used to fetch the poster of the book.
        It takes a single parameter:
        suggested: The suggested books.
        It returns:
        None
        """
        try:
            book_name = []
            ids_index = []
            poster_url = []
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
            final_rating = pickle.load(open(self.recommendation_config.final_rating_serialized_objects, 'rb'))

            for book_id in suggestion:
                book_name.append(book_pivot.index[book_id])

            for name in book_name[0]:
                ids = np.where(final_rating['title'] == name)[0][0]
                ids_index.append(ids)

            for idx in ids_index:
                url = final_rating.iloc[idx]['image_url']
                poster_url.append(url)

            return poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def recommend_book(self, book_name):
        """
        This method is used to recommend the books.
        It takes a single parameter:
        book_name: The name of the book.
        """

        try:
            books_list = []
            model = pickle.load(open(self.recommendation_config.trained_model_path, 'rb'))
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)

            poster_url = self.fetch_poster(suggestion)

            for i in range(len(suggestion)):
                books = book_pivot.index[suggestion[i]]
                for j in books:
                    books_list.append(j)
            return books_list, poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def train_engine(self):
        """
        This method is used to train the engine.
        It takes a single parameter:
        None
        It returns:
        None
        """
        try:
            obj = TrainingPipeline()
            obj.start_training_pipeline()
            st.success("Training Completed!")
            logging.info(f"Recommended successfully!")
        except Exception as e:
            raise AppException(e, sys) from e
        
    def recommendations_engine(self, selected_books):
        """
        This method is used to recommend the books.
        It takes a single parameter:
        selected_books: The selected books.
        It returns:
        None
        """
        try:
            with st.spinner('Fetching recommendations...'):
                recommended_books, poster_url = self.recommend_book(selected_books)
            
            st.subheader("Here are your recommendations:")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_books[1])
                st.image(poster_url[1])
            with col2:
                st.text(recommended_books[2])
                st.image(poster_url[2])
            with col3:
                st.text(recommended_books[3])
                st.image(poster_url[3])
            with col4:
                st.text(recommended_books[4])
                st.image(poster_url[4])
            with col5:
                st.text(recommended_books[5])
                st.image(poster_url[5])
        except Exception as e:
            st.error("Could not generate recommendations. Please try another book or train the engine.")


def main():
    st.set_page_config(page_title="Book Recommender", page_icon="📚")

    # Custom CSS for styling
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 10px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
    }
    
    p {
        color: #333333;
    }

    div.stButton > button {
        background-color: #1E90FF;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #1E90FF;
        padding: 10px 20px;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: white;
        color: #1E90FF;
    }
    
    div[data-testid="stSelectbox"] > label {
        color: #333333 !important;
        font-size: 1.1em;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.9);
        color: black;
    }
    
    .stImage > img {
        border-radius: 10px;
        border: 3px solid #1E90FF;
    }
    
    .stText {
        font-weight: bold;
        color: #333333;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title('📚 Book Recommender System')
    st.markdown("Discover your next favorite book with our collaborative filtering based recommendation system!")

    recommend = Recommendation()

    with st.container():
        st.subheader("Train the Recommendation Engine")
        st.markdown("Click the button below to train the model with the latest data. This might take a few moments.")
        if st.button('Train Recommender System'):
            with st.spinner('Training in progress... please wait.'):
                recommend.train_engine()

    with st.container():
        st.subheader("Get Book Recommendations")
        book_names = pickle.load(open(recommend.recommendation_config.book_name_serialized_objects, 'rb'))
        selected_books = st.selectbox(
            "Type or select a book from the dropdown",
            book_names)
        
        if st.button('Show Recommendation'):
            recommend.recommendations_engine(selected_books)


if __name__ == "__main__":
    main()


