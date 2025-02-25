# Use the official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy only the requirements file first for better caching
COPY requirements.txt .

# Install dependencies, including Uvicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app files into the container
COPY . .

# Expose the port FastAPI runs on
EXPOSE 3005

# Use explicit entrypoint to avoid issues with $PATH
ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3005", "--reload"]
