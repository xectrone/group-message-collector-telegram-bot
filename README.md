# Group Message Collector Bot
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.20-green)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-20.5-blue)

**Group Message Collector** is a robust Telegram bot that helps you manage and organize messages within your Telegram groups. By capturing and storing messages, user details, and group information in a structured database, it provides a seamless way to keep track of your community’s conversations.

## Key Features

- **Message Logging**: Automatically logs and organizes all messages from your group chats.
- **User Management**: Tracks user properties and stores them in a dedicated table for easy access.
- **Group Details**: Captures group-specific attributes, helping you manage multiple groups effortlessly.
- **Efficient Data Retrieval**: Utilizes relational database models to facilitate quick and efficient data queries.
- **Admin Commands**: Includes special commands for admins to manage and retrieve data.

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#1-clone-the-repository)
  - [Install Dependencies](#2-install-dependencies)
  - [Configuration](#3-configuration)
  - [Running the Bot](#4-running-the-bot)
- [Usage](#usage)
  - [Bot Commands](#bot-commands)
  - [Admin Features](#admin-features)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- **Python 3.7+**: Make sure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/).
- **Telegram Bot**: You need a Telegram bot token from [BotFather](https://t.me/BotFather). Follow the instructions to create your bot and get the token.

### 1. Clone the Repository

Open your terminal and navigate to the directory where you want to store the bot's code. Then run:

```bash
git clone https://github.com/xectrone/group-message-collector-telegram-bot.git
```

Navigate into the cloned directory:

```bash
cd group-message-collector-telegram-bot
```

### 2. Install Dependencies

Ensure you are in the project directory and then install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project directory with the following content, replacing the placeholders with your actual Bot Token and Admin IDs:

```plaintext
BOT_TOKEN='YOUR_BOT_TOKEN'
ADMIN_IDS='ID_1,ID_2,ID_3'
```

### 4. Running the Bot

Start the bot by running the following command:

```bash
python bot.py
```

### 5. Enable Message Access

In the BotFather chat, use the `/setprivacy` command, select your bot, and choose "Disable". This setting allows the bot to read all messages in the group, which is necessary for it to log them.

## Usage

### Bot Commands

- `/start` - Start the bot and get a welcome message.
- `/help` - Display all available commands and their descriptions.
- `/all_users` - (Admin) Get a list of all users tracked by the bot.
- `/msgs <UserID>` - (Admin) Retrieve the last 4 messages from a specified user.

### Admin Features

Admin commands require the sender to be listed in the `ADMIN_IDS` in the `.env` file. This ensures that only authorized users can access sensitive information and administrative features.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
