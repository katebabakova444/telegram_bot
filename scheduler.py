from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json
import requests
from dotenv import load_dotenv
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
load_dotenv()
from config import TOKEN, CHAT_ID

def send_scheduled_message():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"🕒 Checking for scheduled messages at {now}")
    try:
        with open("messages_by_date.json", "r", encoding='utf-8') as f:
            messages = json.load(f)
        if now in messages:
            print(f"Sending ID:{CHAT_ID}")
            text = messages[now]
            print(f"📨 Sending: {text}")
            url = f"https://api.telegram.org/bot8478592431:AAHHZ-WlO31WsRLd5gwHz87gXlE5EetZqdI/sendMessage"
            print(f"URL:{url}")
            data = {"chat_id": CHAT_ID, "text": text}
            response = requests.post(url, data=data)
            print(response.status_code)
            print(response.text)
            return response
    except Exception as e:
        print(f"⚠️ Error in scheduler: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_scheduled_message, 'interval', minutes=1)
    scheduler.start()
