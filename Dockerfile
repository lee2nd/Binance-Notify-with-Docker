# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install python-binance
RUN pip install git+https://github.com/Wyattjoh/pushover

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Define environment variable
ENV NAME World