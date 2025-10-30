import json
import random
import schedule
import time
from telegram import Bot
from dotenv import load_dotenv
import os
import threading
from datetime import datetime, date, timedelta
from get_chat_id import BOT_TOKEN

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

with open("messages.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

def send_daily_message():
    if messages:
        msg = messages.pop(0)
        text = f"{msg['message']}\n\nLocation:{msg['location']}"

        bot.send_message(chat_id=CHAT_ID, text=text)

        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

    else:
        bot.send_message(chat_id=CHAT_ID, text=" ")

schedule.every().day.at("10:11").do(send_daily_message)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    t = threading.Thread(target=run_scheduler)
    t.start()
    print("Bot is working.. Waiting for 10:11")