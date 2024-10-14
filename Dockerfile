# Use a Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Introduce dummy secrets for testing
# Hardcoded API key
ENV API_KEY="12345-abcde-67890-fghij"

# Hardcoded password (bad practice, used here only for testing purposes)
RUN echo "DATABASE_PASSWORD='supersecretpassword'" > /app/credentials.txt

# Another example of sensitive information
RUN echo "AWS_SECRET_ACCESS_KEY='EXAMPLEAWSSECRETKEY'" >> /app/credentials.txt

# Copy the rest of the app code
COPY . /app

# Expose the application port (optional, depends on your Flask config)
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
