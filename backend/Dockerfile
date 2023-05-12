FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y sqlite3

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/
RUN rm /app/ase.db
# Create SQLite3 database and import schema
RUN sqlite3 /app/ase.db < /app/init.sql

# Make port 9095 available to the world outside this container
EXPOSE 9095

# Run the command to start the Flask application
CMD ["python", "-m", "src.ase.app"]
