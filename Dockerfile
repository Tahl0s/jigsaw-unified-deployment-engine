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
  && rm -rf /var/lib/apt/lists/*

# Clone the repository from GitHub (replace with your repo URL)
RUN git clone https://github.com/Tahl0s/jigsaw-unified-deployment-engine.git /app

# Install dependencies from requirements.txt inside the repo
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Download the llama3 model (assuming you can pull it via a URL or it needs to be placed locally)
RUN curl -o /app/llama3_model.tar.gz <model_download_url> \
    && tar -xvzf /app/llama3_model.tar.gz -C /app/llama3_model \
    && rm /app/llama3_model.tar.gz

# Stage 2: Final image (only necessary files)
FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=main-app-flask.py \
    FLASK_ENV=production

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source code (already cloned in builder stage)
COPY --from=builder /app /app

# Copy the llama3 model into the image (if it was downloaded in the builder stage)
COPY --from=builder /app/llama3_model /app/llama3_model

# Install necessary dependencies for running the llama3 model (if needed)
# For example, you might need to install Ollama or other model dependencies
RUN pip install --no-cache-dir ollama

# Expose Flask port
EXPOSE 5000

# Start the llama3 model in the background before starting Flask
CMD /bin/bash -c "ollama start --model /app/llama3_model & gunicorn --bind 0.0.0.0:5000 main-app-flask:app"
