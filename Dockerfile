FROM python:3.11-slim

WORKDIR /app

# Set timezone to Asia/Tokyo
ENV TZ=Asia/Tokyo

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt