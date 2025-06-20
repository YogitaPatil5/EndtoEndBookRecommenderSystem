# End-to-End Book Recommender System

This repository contains the source code for a complete end-to-end book recommendation system. The system is built using collaborative filtering and is deployed as a user-friendly web application using Streamlit. The entire project is containerized with Docker for easy deployment and scalability.

## 🌟 Features

- **Collaborative Filtering:** Recommends books based on the ratings of similar users.
- **Interactive Web UI:** A beautiful and intuitive web interface built with Streamlit.
- **Modular ML Pipeline:** A structured and reproducible pipeline for data ingestion, validation, transformation, and model training.
- **Production-Ready:** Code is organized, documented, and containerized for real-world deployment.
- **Containerized:** Includes a `Dockerfile` for easy setup and deployment in any environment.

## 🚀 Project Workflow

The project follows a standard machine learning pipeline workflow, orchestrated to ensure robustness and reproducibility.

1.  **Data Ingestion:** The pipeline begins by downloading a dataset of book ratings from a remote source. It's designed to be idempotent, skipping the download if the data already exists.
2.  **Data Validation:** The raw data is validated against a predefined schema to ensure data quality. This step checks for correct columns and data types, preventing errors in later stages.
3.  **Data Transformation:** The validated data undergoes a series of transformations. This includes cleaning, renaming columns, filtering out less active users and less popular books, merging datasets, and finally, creating a user-item pivot table.
4.  **Model Training:** A K-Nearest Neighbors (KNN) model is trained on the final pivot table. The trained model is then serialized and saved as a pickle file.
5.  **Web Application:** The Streamlit application loads the saved model and other artifacts to provide book recommendations to the user through an interactive interface.

## ⚙️ How to Run the Project

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.8 or higher
- A virtual environment tool (like `venv` or `conda`)

### 1. Clone the Repository

```bash
git clone https://github.com/YogitaPatil5/EndtoEndBookRecommenderSystem.git
cd EndtoEndBookRecommenderSystem
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

**Using `conda`:**
```bash
conda create --name bookrec python=3.9 -y
conda activate bookrec
```

**Using `venv`:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

The project's dependencies are listed in `requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```
This will install all necessary packages, including your local `books_recommender` source code in editable mode.

### 4. Run the Training Pipeline

Before running the web application for the first time, you need to run the training pipeline to generate the necessary model and data artifacts.

You can run the pipeline by executing the `main.py` script:
```bash
python main.py
```
Alternatively, you can trigger the training from the web application's UI.

### 5. Run the Streamlit Web Application

Once the training pipeline has completed successfully, you can start the web application:

```bash
streamlit run app.py
```
This will open the application in your default web browser.

## 🐳 How to Run with Docker

This project is fully containerized, allowing you to run it without worrying about local dependencies.

### Prerequisites
- Docker installed and running on your machine.

### 1. Build the Docker Image

From the root directory of the project, run the following command to build the Docker image:
```bash
docker build -t book-recommender .
```

### 2. Run the Docker Container

Once the image is built, you can run it as a container:
```bash
docker run -p 8501:8501 book-recommender
```
This will start the Streamlit application. You can access it in your browser at `http://localhost:8501`.

## 📁 Project Structure

The project follows a modular structure to ensure clarity and maintainability.

```
.
├── app.py                  # Main script for the Streamlit web application
├── books_recommender/      # Core source code for the ML application
│   ├── __init__.py
│   ├── components/         # Contains individual pipeline components
│   │   ├── stage_00_data_ingestion.py
│   │   ├── stage_01_data_validation.py
│   │   ├── stage_02_data_transformation.py
│   │   └── stage_03_model_trainer.py
│   ├── config/             # Configuration management
│   │   └── configuration.py
│   ├── constant/           # Project-wide constants
│   ├── entity/             # Data entity definitions (e.g., config classes)
│   ├── exception/          # Custom exception handling
│   ├── logger/             # Logging setup
│   ├── pipeline/           # ML pipeline orchestration
│   │   └── training_pipeline.py
│   └── utils/              # Utility functions
├── config/                 # Project configuration files
│   └── config.yaml
├── Dockerfile              # Instructions for building the Docker image
├── LICENSE                 # Project license
├── main.py                 # Main script to run the training pipeline
├── notebook/               # Jupyter notebooks for experimentation
├── README.md               # This file
├── requirements.txt        # Project dependencies
└── setup.py                # Setup script for installing the local package
```

Thank you for exploring the End-to-End Book Recommender System!







