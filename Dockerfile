# Base image
FROM python:3.11 AS base

# Set the working directory in the container
WORKDIR /app

# Install unzip and curl
RUN apt-get update && apt-get install -y unzip curl

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Update the PATH to include the Poetry binary
ENV PATH="/root/.local/bin:${PATH}"

# Copy only the pyproject.toml and poetry.lock (if it exists)
COPY pyproject.toml poetry.lock* /app/

# Install the project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app

# Add the application root to PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose the port the app runs on
EXPOSE 8501

# Set the command to run the app
CMD ["poetry", "run", "streamlit", "run", "presentation/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]