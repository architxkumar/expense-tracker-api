# Use an official lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cloud Run will tell us which port to use
ENV PORT=8080

# Set working directory inside container
WORKDIR /app

# Install system dependencies required for psycopg / asyncpg builds
RUN apt-get update && apt-get install -y build-essential

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . .

# Cloud Run ignores EXPOSE but it doesn’t harm
EXPOSE 8080

# Run the FastAPI app using the dynamic Cloud Run PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
