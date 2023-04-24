# Discord Log Bot

This is a simple Discord bot written in Python that logs events happening in a server such as voice joins, leaves, moves, role edits, and message deletions. The logs are stored in a designated text channel.

## Prerequisites

- Python 3.6 or higher
- pip
- A Discord account and server
- A Discord bot token (follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html) to create a bot and get its token)

## Installation and Usage

1. Clone this repository or download the ZIP file and extract it to your desired location.
2. Navigate to the project directory in a terminal or command prompt.
3. Install the required Python packages by running the following command: `pip install -r requirements.txt`.
4. Create a `.env` file in the project directory with the following contents:
   - `TOKEN`: Your Discord bot token.
   - `LOG_CHANNEL_ID`: The ID of the channel where you want the bot to send logs.
 
Replace `<your_bot_token>` with your actual bot token and `<your_log_channel_id>` with the ID of the text channel where you want to store the logs. 
You can find the channel ID by enabling Developer Mode in Discord (under User Settings > Appearance) and then right-clicking on the desired channel and selecting "Copy ID".
5. Start the bot by running the following command: `python bot.py`.

The bot should now be online and logging events to the specified channel.

## Using Docker

Alternatively, you can use Docker to run the bot in a container. To do this, follow these steps:

1. Install Docker on your machine (see [here](https://docs.docker.com/get-docker/) for instructions).
2. Clone this repository or download the ZIP file and extract it to your desired location.
3. Navigate to the project directory in a terminal or command prompt.
4. Build the Docker image by running the following command: `docker build -t log-bot .`.
5. Create a `.env` file in the project directory with the following contents:
   - `BOT_TOKEN=<your_bot_token>`
   - `LOG_CHANNEL_ID=<your_log_channel_id>`
Replace `<your_bot_token>` with your actual bot token and `<your_log_channel_id>` with the ID of the text channel where you want to store the logs. You can find the channel ID by enabling Developer Mode in Discord (under User Settings > Appearance) and then right-clicking on the desired channel and selecting "Copy ID".
6. Start the Docker container by running the following command: `docker run --env-file .env log-bot`.

The bot should now be running inside a Docker container and logging events to the specified channel.

## Contributing

If you find any bugs or have suggestions for new features, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
