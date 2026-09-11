# Use a slim Python image (smaller than the default)
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the API requirements first (for better caching)
COPY requirements-api.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-api.txt

# Copy the rest of the application code
COPY app/ ./app/

# Expose port 8000 (documentation only, doesn't actually publish it)
EXPOSE 8000

# The command to run when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]