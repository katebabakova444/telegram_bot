from flask import Flask, request
import asyncio
from datetime import datetime
import json
import os
import aiohttp

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

async def send_daily_message():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"⏰ Проверка времени: {now}")

    with open('messages_by_date.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)

    if now in messages:
        text = messages[now]
        print(f"📤 Отправка сообщения: {text}")
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {"chat_id": CHAT_ID, "text": text}
            async with session.post(url, data=payload) as resp:
                print(f"🔄 Статус отправки: {resp.status}")
    else:
        print("🕐 Сообщения не запланированы на это время.")

async def scheduler_loop():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        if now.endswith("00") or now.endswith("30"):
            await send_daily_message()
            await asyncio.sleep(61)
        else:
            await asyncio.sleep(20)

@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        data = await request.get_json(force=True)
        print(f"Webhook received data: {data}")
        return "OK"
    except Exception as e:
        print(f"Webhook error: {e}")
        return f"Internal Server Error: {e}", 500

@app.route("/")
def home():
    return "Telegram bot is running."

def start_scheduler():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(scheduler_loop())
    loop.run_forever()

if __name__ == "__main__":
    from threading import Thread
    Thread(target=start_scheduler).start()
    app.run(host="0.0.0.0", port=4545)