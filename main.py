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
with open("messages.json", "r", encoding="utf-8") as f:
    data = json.load(f)
messages_by_date = {item["date"]: item["message"] for item in data}
with open("mesages_by_date.json", "w", encoding="utf-8") as f:
    json.dump("messages_by_date.json", "w", ensure_ascii=False, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working!")


async def send_daily_message():
    now = datetime.now().strftime("%H:%M")
    try:
        with open("messages_by_date.json", "r", encoding="utf-8") as f:
            messages = json.load(f)
        now = datetime.now().strftime("%Y-%m-%d%T%H")
        text = messages.get(now, None)
        if text:
            await app.bot.send_message(chat_id=CHAT_ID, text=text)
        else:
            print(f"[{now}] No messages.")
    except Exception as e:
        print(f"Error: {e}")

async def scheduler_loop():
    while True:
        await send_daily_message()
        await asyncio.sleep(60)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

async def main():
    asyncio.create_task(scheduler_loop())
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())