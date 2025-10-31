from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json
import requests
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_scheduled_message():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"🕒 Checking for scheduled messages at {now}")
    try:
        with open("messages_by_date.json", "r", encoding='utf-8') as f:
            messages = json.load(f)
        if now in messages:
            text = messages[now]
            print(f"📨 Sending: {text}")
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            data = {"chat_id": CHAT_ID, "text": text}
            response = requests.post(url, data=data)
            print("✅ Sent!" if response.ok else f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"⚠️ Error in scheduler: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_scheduled_message, 'interval', minutes=1)
    scheduler.start()