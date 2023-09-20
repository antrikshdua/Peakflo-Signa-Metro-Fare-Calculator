# Stage 1: Build the application
FROM python:3.8-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#  Create and set the working directory
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code from the build stage
COPY . /code

# Expose the port that the application will run on
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
