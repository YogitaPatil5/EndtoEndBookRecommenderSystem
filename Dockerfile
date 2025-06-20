# 1. Use a modern, supported, and secure Python version
FROM python:3.9-slim-buster

# Expose the port streamlit will run on
EXPOSE 8501

# Install system dependencies and then clean up the cache
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy dependency list and install them to leverage build caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# 2. Create a non-root user and switch to it for security
RUN addgroup --system app && adduser --system --group app
USER app

# The command to run the app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
