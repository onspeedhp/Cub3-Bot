# Cube Exchange Bot

Welcome to the Cube Exchange Bot! This bot is designed to provide real-time cryptocurrency data and manage your Cube Exchange account. It uses the Telegram Bot API to interact with users and perform various actions based on user commands.

## Features

- **Start**: Introduces the bot and its functionalities.
- **Info**: Provides real-time data for specified cryptocurrencies.
- **Orders**: Retrieves and displays your order information.
- **User**: Allows you to manage your account information.
- **Subaccount**: Manages subaccount information.
- **Exit**: Exits the current mode and resets the state.

## Getting Started

### Prerequisites

- Python 3.7+
- Telegram Bot API token
- Cube Exchange API key and secret

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/cube-exchange-bot.git
    cd cube-exchange-bot
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your Telegram Bot API token:

    ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    ```

4. Define constants and callback functions in `constant.py` and `callback.py`.

### Running the Bot

To run the bot, execute:

```bash
python bot.py