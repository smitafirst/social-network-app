# # Use the official Python image from the Docker Hub
# FROM python:3.9.6

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory
# WORKDIR /code

# # Install dependencies
# COPY requirements.txt /code/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy the project files
# COPY . /code/

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Expose the port the app runs on
# EXPOSE 8000

# # Run the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#        gcc \
#        libpq-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 for the application
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
