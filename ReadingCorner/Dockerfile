# Use the official Python image as a base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies and clean up the cache in one step
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip
##
# Copy requirements first to leverage Docker cache
COPY ReadingCorner/requirements.txt /app/

# Install Python dependencies, avoid caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the application's port (adjust if necessary for production)
EXPOSE 8000

# Run the application (ensure this is appropriate for production, or use gunicorn in production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
