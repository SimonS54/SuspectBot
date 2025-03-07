# SuspectBot

![SuspectBot Banner](https://i.postimg.cc/j2MLDXtN/image-2025-02-26-202640196.png)  
*A powerful Discord bot designed to streamline support, moderation, and customer interaction for gaming communities.*

## Overview

SuspectBot is a versatile Discord bot built with Python and the `discord.py` library, integrated with Firebase Firestore for data persistence and OpenAI for AI-powered ticket assistance. It provides a wide range of features including support tools, moderation utilities, payment guides, documentation, message filtering, and staff performance tracking. Whether you're managing a gaming community or a customer support server, SuspectBot is here to enhance your workflow.

## Features

- **Support Tools**: Guides for virtualization, TPM, Secure Boot, and dependency installation, plus remote support via AnyDesk.
- **Moderation**: Send announcements, updates, and manage product statuses with interactive buttons.
- **Payment Instructions**: Step-by-step guides for payments via middlemen (e.g., Dat, Paradox).
- **Documentation**: Detailed setup guides for various gaming products (e.g., Apex Lite, Rust Fluent).
- **Message Filtering**: Automatically filter messages in specified channels based on allowed words, with logging.
- **AI Assistant**: AI-driven ticket support with response suggestions, staff review via reactions, and fine-tuning capabilities.
- **Staff Stats**: Track ticket-handling performance for staff members (daily, weekly, monthly, total).
- **Elitepvpers Integration**: Guides for leaving vouches and trade reviews on Elitepvpers.
- **Error Fixes**: Comprehensive error code solutions for supported products.
- **General Utilities**: Command list (`/bothelp`) and review submission functionality.

## Installation

### Prerequisites
- Python 3.8+
- Discord bot token (obtained from the [Discord Developer Portal](https://discord.com/developers/applications))
- Firebase project with a service account key (`suspectbotdb.json`)
- OpenAI API key (for AI features)
- Required Python packages: `discord.py`, `firebase-admin`, `openai`, `python-dotenv`, `Levenshtein`

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/suspectbot.git
   cd suspectbot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the root directory:
   ```plaintext
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   Place your Firebase service account key (`suspectbotdb.json`) in the `data/` directory.

4. **Configure the Bot**
   Edit `cogs/config.py` with your server-specific role IDs, channel IDs, and category IDs (see Configuration below).

5. **Run the Bot**
   ```bash
   python main.py
   ```

## License

This project is licensed under the MIT License - see the LICENSE section below.