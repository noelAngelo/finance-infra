# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src

# Install Poetry
RUN pip install poetry

# Copy only the necessary folders
COPY app ./app
COPY config ./config

# Copy Poetry files
COPY pyproject.toml ./

# Install dependencies
RUN poetry install --no-root

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the FastAPI application
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]