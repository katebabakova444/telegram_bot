import asyncio
import json
import os
from datetime import datetime
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import schedule
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working!")


async def send_daily_message():
    now = datetime.now().strftime("%H:%M")
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            messages = json.load(f)
        text = messages.get(now, "")
        if text:
            await app.bot.send_message(chat_id=CHAT_ID, text=text)
        else:
            print(f"[{now}] No messages.")
    except Exception as e:
        print(f"Error: {e}")

def schedule_jobs():
    with open("messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
    for time_str in messages.keys():
        schedule.every().day.at(time_str).do(lambda: asyncio.create_task(send_daily_message()))


async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

async def main():
    schedule_jobs()
    asyncio.create_task(scheduler_loop())
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())