# 🐳 DoseSafe AI - Optimized Multi-stage Docker Build

# Build stage for frontend
FROM node:18-alpine AS frontend-builder
LABEL stage=frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.10-slim AS production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    tesseract-ocr \
    tesseract-ocr-eng \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy backend code
COPY backend/ ./backend/
COPY ml_models/ ./ml_models/

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend/dist ./static

# Create necessary directories
RUN mkdir -p uploads database

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV DEBUG=False

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Switch to backend directory and run
WORKDIR /app/backend
CMD ["python", "app.py"]

# Start command
CMD ["python", "start_production.py"]
