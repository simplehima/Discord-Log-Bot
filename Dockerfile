FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies in the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the container
COPY . .

# Set environment variables
# ENV LOG_CHANNEL_ID=<insert log channel ID here>
# ENV TOKEN=<insert bot token here>

# Run the bot
CMD ["python", "bot.py"]
