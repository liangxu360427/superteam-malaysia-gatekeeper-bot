#!/usr/bin/env python3
"""
Superteam Malaysia Telegram Intro Gatekeeper Bot
=================================================
Bounty: Build a Telegram Intro Gatekeeper Bot for Superteam
"""
import os
import logging
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

DB_NAME = 'introductions.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS introductions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER, username TEXT, first_name TEXT, last_name TEXT,
                  name TEXT, background TEXT, motivation TEXT,
                  telegram_link TEXT, twitter_link TEXT, linkedin_link TEXT,
                  status TEXT DEFAULT 'pending',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

NAME, BACKGROUND, MOTIVATION, LINKS = range(4)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = "Welcome to Superteam Malaysia! Let's get started. Please enter your full name:"
    await update.message.reply_text(welcome)
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data['name'] = name
    await update.message.reply_text(f"Great {name}! Now tell us about your background (profession, skills, experience):")
    return BACKGROUND

async def get_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    background = update.message.text
    context.user_data['background'] = background
    await update.message.reply_text("Why do you want to join Superteam Malaysia? What are you hoping to gain?")
    return MOTIVATION

async def get_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    motivation = update.message.text
    context.user_data['motivation'] = motivation
    await update.message.reply_text("Share your social links (optional): Telegram @username, Twitter @username, LinkedIn URL")
    return LINKS

async def get_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    links = update.message.text
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO introductions 
                 (user_id, username, first_name, last_name, name, background, motivation)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (user.id, user.username, user.first_name, user.last_name,
               context.user_data.get('name'), context.user_data.get('background'),
               context.user_data.get('motivation')))
    conn.commit()
    conn.close()
    
    await update.message.reply_text("Application submitted! Our team will review within 48 hours.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled. Use /start to begin again.")
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Begin\n/help - Help\n/status - Check status")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT name, status FROM introductions WHERE user_id = ?', (user.id,))
    result = c.fetchone()
    conn.close()
    if result:
        await update.message.reply_text(f"Name: {result[0]}\nStatus: {result[1]}")
    else:
        await update.message.reply_text("No application. Use /start")

def main():
    init_db()
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
                BACKGROUND: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_background)],
                MOTIVATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_motivation)],
                LINKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_links)]},
        fallbacks=[CommandHandler('cancel', cancel)])
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('status', status_command))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()