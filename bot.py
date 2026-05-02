import requests
import os
import time
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def send_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=starknet,owb&vs_currencies=usd&include_24hr_change=true"
        data = requests.get(url).json()
        
        strk = data["starknet"]
        owb = data["owb"]
        
        msg = f"""🕒 <b>Цены STRK vs OWB</b>

STRK: ${strk['usd']:.4f} ({strk.get('usd_24h_change',0):+.1f}%)
OWB: ${owb['usd']:.4f} ({owb.get('usd_24h_change',0):+.1f}%)"""
        
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='HTML')
        print("Сообщение отправлено")
    except Exception as e:
        print("Ошибка:", e)

send_prices()   # отправить сразу
print("Бот отработал")
