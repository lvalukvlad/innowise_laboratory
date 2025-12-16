# Use official Python slim image
FROM python:3.11-slim
# Set working directory
WORKDIR /app
# Copy requirements
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy application code and database
COPY app.py .
COPY books.db .
# Expose port
EXPOSE 8000
# Start application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]