# Superteam Malaysia Telegram Intro Gatekeeper Bot

A production-ready Telegram bot for managing community introductions for Superteam Malaysia.

## Bounty Submission

- **Bounty**: Build a Telegram Intro Gatekeeper Bot for Superteam
- **Prize**: 1,000 USDG
- **Sponsor**: Superteam Malaysia

## Features

### Core Functionality
- **Multi-step Introduction Flow**: Collected name, background, motivation, and social links
- **SQLite Database**: Stores all submissions locally
- **Status Checking**: Users can check their application status
- **Admin Commands**: List all submissions (expandable)

### Bot Commands
- `/start` - Begin introduction process
- `/help` - Show help message
- `/status` - Check your application status
- `/cancel` - Cancel current conversation

### Data Collected
1. Full Name
2. Professional Background (skills, experience)
3. Motivation for joining
4. Social Media Links (Telegram, Twitter, LinkedIn)

## Technical Architecture

```
User -> Telegram Bot -> Conversation Handler -> SQLite Database
                                      |
                                      v
                              Introduction Stored
                                      |
                                      v
                              Admin Review
```

## Installation

```bash
# Clone the repository
git clone https://github.com/liangxu360427/superteam-malaysia-gatekeeper-bot
cd superteam-malaysia-gatekeeper-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export TELEGRAM_BOT_TOKEN=your_bot_token_here

# Run the bot
python main.py
```

## Deployment

### Option 1: Render.com (Free)
1. Push code to GitHub
2. Connect GitHub to Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`
5. Add environment variable `TELEGRAM_BOT_TOKEN`

### Option 2: VPS/Server
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip
git clone <repo>
cd <repo>
pip install -r requirements.txt
nohup python main.py &

# Or use systemd for production
```

### Option 3: Railway
1. Connect GitHub repo to Railway
2. Add TELEGRAM_BOT_TOKEN in env vars
3. Deploy!

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| TELEGRAM_BOT_TOKEN | Yes | Your bot token from @BotFather |

## Obtaining Telegram Bot Token

1. Open Telegram and search for @BotFather
2. Use /newbot command
3. Follow prompts to name your bot
4. Copy the API token

## Database Schema

```sql
CREATE TABLE introductions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    name TEXT,
    background TEXT,
    motivation TEXT,
    telegram_link TEXT,
    twitter_link TEXT,
    linkedin_link TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Project Structure

```
superteam-malaysia-gatekeeper-bot/
├── main.py              # Main bot code
├── requirements.txt     # Python dependencies  
├── README.md           # This file
└── introductions.db    # SQLite database (created on first run)
```

## License

MIT

## Author

- GitHub: liangxu360427
- Telegram: Your username

## Notes

This bot is submitted as a bounty entry for Superteam Malaysia's Telegram Intro Gatekeeper Bot requirement. It includes:
- Complete conversation flow
- Database storage
- Status checking
- Production-ready error handling
- Easy deployment options