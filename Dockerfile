# Use Python 3.10 as the base image
FROM python:3.10

# Update package list and install necessary system packages
RUN apt update && apt upgrade -y && apt install git -y

# Copy requirements.txt into the container
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the working directory
COPY . .

# Expose port 8080 to allow access to the web server
EXPOSE 8080

# Set the command to run the bot
CMD ["python", "bot.py"]

