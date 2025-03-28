# Stage 1: Builder (for dependencies)
FROM python:3.9-slim AS builder

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required for some Python packages (e.g., NumPy, Pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -sSL https://ollama.com/install.sh | bash

# Clone the repository from GitHub
RUN git clone https://github.com/Tahl0s/jigsaw-unified-deployment-engine.git /app

# Install dependencies from requirements.txt inside the repo
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Stage 2: Final image (only necessary files)
FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=main-app-flask.py \
    FLASK_ENV=production

# Install curl and Ollama in the final image
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -sSL https://ollama.com/install.sh | bash

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source code (already cloned in builder stage)
COPY --from=builder /app /app

# Expose Flask port
EXPOSE 5000

# Add a healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000 || exit 1

# Start Ollama to pull and run the model, then run the Flask application
CMD ["sh", "-c", "ollama pull llama3 && ollama run llama3 & gunicorn --bind 0.0.0.0:5000 --timeout 300 main-app-flask:app"]

