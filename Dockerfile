# Use official Python runtime as base image
FROM python:3.12-slim-bookworm AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=/app

# Set work directory
WORKDIR /app

## Install system dependencies required for building Python packages
#RUN apt-get update && apt-get install -y \
#    build-essential \
#    libpq-dev \
#    python3-dev \
# Install system dependencies required for building Python packages (including WeasyPrint)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    # Clean up build dependencies to reduce image size
    apt-get purge -y --auto-remove build-essential python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Production stage
FROM python:3.12-slim-bookworm AS production

# Security best practices: Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# Install runtime system dependencies (including WeasyPrint runtime libraries)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Install system dependencies required for runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq5 \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Create font cache directory with proper permissions
RUN mkdir -p /tmp/.cache/fontconfig && \
    chown -R appuser:appuser /tmp/.cache && \
    chmod -R 755 /tmp/.cache

RUN mkdir -p /app && chown appuser:appuser /app
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create static directory with proper permissions
RUN mkdir -p /app/collected_static && \
    chown -R appuser:appuser /app/collected_static/ && \
    chmod -R 755 /app/collected_static/

# Copy and make entrypoint script executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user
USER appuser

# Copy application code
COPY --chown=appuser:appuser . .
# Copy installed Python packages
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code
COPY --from=builder /app .