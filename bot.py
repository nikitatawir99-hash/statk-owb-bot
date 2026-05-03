import requests
import os
import time
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("Бот стартовал")

bot = Bot(token=BOT_TOKEN)

try:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=starknet,owb&vs_currencies=usd&include_24hr_change=true"
    data = requests.get(url).json()
    
    strk = data["starknet"]
    owb = data["owb"]
    
    msg = f"STRK: ${strk['usd']:.4f} ({strk.get('usd_24h_change',0):+.1f}%)\n"
    msg += f"OWB: ${owb['usd']:.4f} ({owb.get('usd_24h_change',0):+.1f}%)"
    
    bot.send_message(chat_id=CHAT_ID, text=msg)
    print("Сообщение отправлено успешно")
except Exception as e:
    print("Ошибка:", str(e))

print("Скрипт завершён")
time.sleep(300)  # 5 минут
