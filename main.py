import json
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
import asyncio
import os
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
WEBHOOK_URL = 'https://telegram-bot-1-wdbm.onrender.com/webhook'

app = Flask(__name__)
bot = Bot(token=TOKEN)
tg_app = ApplicationBuilder().token(TOKEN).build()
MESSAGES_FILE = "messages_by_date.json"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working via webhook!")

async def send_daily_message():
    try:
        now = datetime.now().strftime("%Y-%m-%dT%H")
        with open("messages_by_date.json", "r", encoding="utf-8") as f:
            messages = json.load(f)
        if now in messages:
           text = messages[now]
           await tg_app.bot_initialize()
           await tg_app.bot.send_message(chat_id=CHAT_ID, text=text)
           print(f"[{now}] Message send: {text}")
        else:
            print(f"[{now}] No message.")
    except Exception as e:
        print(f"Error: {e}")


async def scheduler_loop():
    while True:
        now = datetime.now().strftime("%Y-%m-%dT%H")
        if now.endswith("00") or now.endswith("30"):
            await send_daily_message()
            await asyncio.sleep(61)
            print(datetime.now())
        else:
            await asyncio.sleep(20)

@app.route("/webhook", methods=['POST'])
async def webhook():
    try:
        data = request.get_json(force=True)
        print(f"Webhook received data: {data}")
        return "OK"
    except Exception as e:
        print(f"Webhook error: {e}")
        return f"Internal Server Error: {e}", 200
@app.route("/")
def home():
    return "Telegram bot is running"
@app.before_request
def activate_scheduler():
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_loop())



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 4545)))

