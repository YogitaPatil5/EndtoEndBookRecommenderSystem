# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the container
COPY . .

# Switch to the non-root user
USER app

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
