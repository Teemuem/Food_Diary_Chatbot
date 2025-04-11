# Use a Python 3.12 base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Create upload directory
RUN mkdir -p /app/uploaded_images

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

EXPOSE 8501

# Define environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501

# Run Streamlit when the container launches
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]