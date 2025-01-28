# Stage 1: Build stage
FROM python:3.10-slim AS build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set up virtual environment
RUN python3 -m venv /env

# Set environment variables to use the virtual environment
ENV PATH="/env/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.10-slim

# Copy only necessary files from the build stage
COPY --from=build /env /env

# Set environment variables to use the virtual environment
ENV PATH="/env/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Set the user
RUN addgroup app && adduser --system --ingroup app app
USER app

# Run the Django application
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
