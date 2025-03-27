# Build stage: Install dependencies and setup virtual environment

FROM python:3.12-slim AS builder

# Set the working directory in the container to /app
WORKDIR /app

# Configure Poetry to install the virtualenv in the project folder
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install GCC (required for compiling certain dependencies) and Poetry
RUN apt-get update && apt-get install gcc -y
RUN pip install poetry==2.1.1

# Copy only the Poetry requirements
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY .env .env

# Create the src directory, required for the structure of the project
RUN mkdir -p src 

# Install the dependencies specified in pyproject.toml
RUN poetry install --no-root

# ----------------------------------------------------------------------
# Runtime stage: Set up the container for running the application

FROM builder AS runner

# Set the PYTHONPATH environment variable to the src directory
# This ensures Python can find the rdw module when running the application
ENV PYTHONPATH="/app/src"

# Copy the virtual environment from the builder stage (with all dependencies)
COPY --from=builder /app/.venv /app/.venv

# Copy the source code into the container's src directory
COPY ./src /app/src

# Use Uvicorn to run the FastAPI app, specify host and port
# This will start the app when the container runs
CMD ["poetry", "run", "python", "-u", "src/home_automation/app/main.py"]