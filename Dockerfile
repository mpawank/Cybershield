# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install notebook

# Copy all source code to the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 5000

# Optional: expose Jupyter if you want to use notebooks inside the container
EXPOSE 8888

# Command to run both Flask and Jupyter (you can modify/remove Jupyter if unnecessary)
CMD ["sh", "-c", "flask run & jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token='' --NotebookApp.password=''"]

