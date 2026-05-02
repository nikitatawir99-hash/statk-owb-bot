import requests
import time
import os
from datetime import datetime
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=starknet,owb&vs_currencies=usd&include_24hr_change=true"
    try:
        data = requests.get(url).json()
        strk = data["starknet"]
        owb = data["owb"]
        return strk, owb
    except:
        return None, None

def send_message(text):
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML')

# Первый запуск
strk, owb = get_prices()
if strk and owb:
    msg = f"🕒 <b>Цены обновлены</b>\n\n"
    msg += f"🟢 STRK: ${strk['usd']:.4f} ({strk.get('usd_24h_change',0):+.1f}%)\n"
    msg += f"🟢 OWB: ${owb['usd']:.4f} ({owb.get('usd_24h_change',0):+.1f}%)"
    send_message(msg)

print("Бот запущен")
time.sleep(3600)  # работает 1 час, потом Railway перезапустит
