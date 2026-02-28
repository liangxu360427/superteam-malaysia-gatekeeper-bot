#!/usr/bin/env python3
"""
Superteam Malaysia Telegram Intro Gatekeeper Bot
Bounty Submission - Superteam Earn
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        'Welcome to Superteam Malaysia! Please introduce yourself.'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text('Use /start to begin')

async def handle_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process user introduction"""
    user = update.effective_user
    intro = update.message.text
    logger.info(f'New intro from {user.username}')
    await update.message.reply_text('Thank you! We will review your application.')

def main():
    """Run the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_intro))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()