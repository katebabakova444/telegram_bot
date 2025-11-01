from flask import Flask, request
from scheduler import start_scheduler
import os
from dotenv import load_dotenv

from config import TOKEN, CHAT_ID

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram scheduler bot is running!"
start_scheduler()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
