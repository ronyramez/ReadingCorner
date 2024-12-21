# Use the official Python image as a base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /ReadingCorner

# Install system dependencies
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       build-essential \
    || (sleep 30 && apt-get update --fix-missing && apt-get install -y --no-install-recommends libpq-dev build-essential) \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY ReadingCorner/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the application's port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver"]
