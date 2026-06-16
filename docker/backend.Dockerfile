# Use a slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask flask-cors  # Ensure web-specific dependencies are present

# Copy the entire src directory and project configs
COPY src/ ./src/
COPY pyproject.toml .

# Set Pythonpath so it can find the src modules
ENV PYTHONPATH=/app/src

# Expose the Flask port
EXPOSE 5000

# Run the API
CMD ["python", "src/api/app.py"]
