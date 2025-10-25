# Use a standard Python 3.10 image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY . .

# Cloud Run requires the container to listen on the PORT environment variable (default: 8080)
ENV PORT=8080

# Expose the port
EXPOSE $PORT

# Command to run your FastAPI app
# Uses PORT environment variable from Cloud Run (defaults to 8080)
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}
