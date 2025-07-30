# Use Python 3.11 slim image for smaller footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for video downloading and processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/
COPY README.md ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Install Flask for web UI (add to existing dependencies)
RUN pip install --no-cache-dir flask flask-socketio

# Create downloads directory
RUN mkdir -p /app/downloads

# Expose port for web interface
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Default command - run web interface
CMD ["python", "-m", "aniworld", "--web"]