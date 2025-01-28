# Use the official Python image as the base image
FROM python:3.10-slim

# Set environment variables to prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py  

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip setuptools wheel


RUN pip install -r requirements.txt

# Expose port 8080 for Flask
EXPOSE 8080

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
