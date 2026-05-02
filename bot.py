import requests
import time
import schedule
import os
from datetime import datetime
from telegram import Bot
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

COINS = {
    "starknet": "STRK",
    "owb": "OWB"
}

THRESHOLD = 8.0

async def send_message(text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML')

def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "starknet,owb",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        return {
            "STRK": {"price": data["starknet"]["usd"], "change": data["starknet"].get("usd_24h_change", 0)},
            "OWB": {"price": data["owb"]["usd"], "change": data["owb"].get("usd_24h_change", 0)}
        }
    except:
        return None

def job():
    prices = get_prices()
    if not prices:
        return

    now = datetime.now().strftime("%H:%M")
    msg = f"🕒 <b>Цены на {now} (Киев)</b>\n\n"
    
    for symbol, p in prices.items():
        emoji = "🟢" if p["change"] >= 0 else "🔴"
        msg += f"{emoji} <b>{symbol}</b>: ${p['price']:.4f} ({p['change']:+.1f}%)\n"

    # Алерт при сильном движении
    alert = ""
    for symbol, p in prices.items():
        if abs(p["change"]) >= THRESHOLD:
            dir_text = "🚀 ВЗЛЁТ" if p["change"] > 0 else "📉 ОБВАЛ"
            alert += f"\n\n⚠️ <b>{dir_text} {symbol}!</b> {p['change']:+.1f}% за 24ч"

    if alert:
        msg += alert

    asyncio.run(send_message(msg))

if name == "main":
    print("Бот запущен...")
    schedule.every(6).hours.do(job)
    job()  # первый запуск сразу

    while True:
        schedule.run_pending()
        time.sleep(60)
