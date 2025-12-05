# Use a slim Python image for a smaller footprint
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ ./src/

# Expose the port your Flask app runs on
EXPOSE 8080

# Define environment variables (can be overridden by Kubernetes)
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Run the Flask application
CMD ["python", "src/app.py"]
