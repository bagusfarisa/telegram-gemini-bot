# Telegram Gemini Bot

A Telegram bot that delivers daily news summaries from Indonesia using Google's Gemini AI. The bot is designed to run automatically via GitHub Actions, sending daily updates at 5:00 AM Indonesia time (UTC+7).

## 🌟 Features

- Fetches and summarizes daily news from Indonesia using Google's Gemini AI
- Sends formatted messages to a specified Telegram chat
- Handles long messages by automatically splitting them to comply with Telegram's 4096-character limit
- Runs automatically via GitHub Actions with no need for a dedicated server
- Timezone-aware scheduling (Asia/Jakarta)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/botfather)
- A Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- A Telegram chat ID where the bot will send messages.[How to get one](https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bagusfarisa/telegram-gemini-bot.git
   cd telegram-gemini-bot
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root with the following content:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   GEMINI_API_KEY=your_gemini_api_key
   ```

## 🛠️ Usage

### Running Locally

To test the bot locally:

```bash
python telegram_gemini_bot.py
```

### Setting Up GitHub Actions

The bot is configured to run automatically via GitHub Actions. To set this up:

1. Push the cloned repository to your own repo.
   ```bash
   git remote set-url origin YOUR_NEW_REPOSITORY_URL
   git push -u origin main
   ```
2. Add the following secrets to your repository (Settings > Secrets and variables > Actions):
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: The chat ID where the bot will send messages
   - `GEMINI_API_KEY`: Your Google Gemini API key

3. The workflow is already configured to run daily at 5:00 AM Indonesia time (Asia/Jakarta). You can find the configuration in `.github/workflows/daily-gemini-bot.yml`.

### Manual Trigger

You can manually trigger the workflow from the Actions tab in your GitHub repository by clicking on "Daily Gemini Telegram Bot" and then "Run workflow".

## 🔧 Customization

### Modifying the News Prompt

You can customize the news prompt by editing the `prompt` variable in the `main()` function in `telegram_gemini_bot.py`. The default prompt is:

```python
prompt = """
Give me a brief summary of today's news from Indonesia. 
Focus on 5 most important events and avoid unnecessary details. 
Don't repeat the same news and make sure it's only a single list of news. 
Give short headline for each news with this format '1. {Headline Title}' and then start a new line. 
Give 1 line spacing between news items. Don't use any markdown styling.
"""
```

### Changing the Schedule

To change when the bot sends updates, modify the cron schedule in `.github/workflows/daily-gemini-bot.yml`. The current schedule is set to run at 5:00 AM Indonesia time (22:00 UTC).

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📬 Contact

For any questions or feedback, please open an issue on GitHub.
