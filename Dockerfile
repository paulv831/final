# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Copy the environment file
COPY .env /app/.env

# Install any needed Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install SQLite3 and any required system tools
RUN apt-get update && apt-get install -y sqlite3 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure the database scripts are executable
RUN chmod +x /app/sql/create_db.sh
RUN chmod +x /app/entrypoint.sh

# Define a volume for persisting the database
VOLUME ["/app/db"]

# Expose the application port
EXPOSE 5000

# Run the entrypoint script when the container launches
CMD ["/app/entrypoint.sh"]