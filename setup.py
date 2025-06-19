from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

## edit below variables
REPO_NAME = "ML Based Books Recommender System"

Author_User_Name = "Yogita Patil"
SRC_REPO = "books_recommender"
LIST_OF_REQUIREMENTS = []

setup(
    name=SRC_REPO,
    version="0.0.1",
    author=Author_User_Name,
    description="A small python package for ML based books recommender system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/YogitaPatil5/EndtoEndBookRecommenderSystem",
    author_email="yogita.m.patil.05@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.8",
    install_requires=LIST_OF_REQUIREMENTS
)