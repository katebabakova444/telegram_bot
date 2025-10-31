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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working via webhook!")

async def send_daily_message():
    try:
        now = datetime.now().strftime("%Y-%m-%dT%H")
        with open("messages_by_date.json", "r", encoding="utf-8") as f:
            messages = json.load(f)
        if now in messages:
           text = messages.get[now]
           await bot.send_message(chat_id=CHAT_ID, text=text)
           print(f"[{now}] Message send: {text}")
        else:
            print(f"[{now}] No message.")
    except Exception as e:
        print(f"Error: {e}")


async def scheduler_loop():
    while True:
        await send_daily_message()
        await asyncio.sleep(60)

@app.route("/webhook", methods=['POST'])
async def webhook():
    try:
        data = request.get_json(force=True)
        print(f"Webhook received data: {data}")
        update = Update.de_json(data, bot)
        await tg_app.process_update(update)
        return "OK"
    except Exception as e:
        print(f"Webhook error: {e}")
        return f"Internal Server Error: {e}", 200
@app.route("/")
def home():
    return "Telegram bot is running"


if __name__ == "__main__":
    tg_app.add_handler(CommandHandler("start", start))
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_loop())

    asyncio.get_event_loop().run_until_complete(
        bot.set_webhook(url=WEBHOOK_URL)
    )
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8443)))