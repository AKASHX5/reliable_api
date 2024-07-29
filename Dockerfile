# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to ensure output is logged in real time
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port that the Flask app runs on
EXPOSE 5008

# Command to run the Flask app
CMD ["python", "main.py"]
