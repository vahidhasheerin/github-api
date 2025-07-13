# Use a slim Python base image for smaller size
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Command to run the application
# Use gunicorn for a production-ready WSGI server instead of Flask's built-in development server
# First, add gunicorn to requirements.txt: gunicorn==21.2.0
# Then, use the following CMD:
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

# If you prefer to stick to Flask's built-in server (less suitable for production but simpler for this exercise):
# CMD ["python", "app.py"]
