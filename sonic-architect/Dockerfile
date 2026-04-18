FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio analysis (librosa needs these)
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python"]