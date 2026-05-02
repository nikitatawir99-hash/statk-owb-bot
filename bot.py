import requests
import os
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def price(update: Update, context):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=starknet,owb&vs_currencies=usd&include_24hr_change=true"
    data = requests.get(url).json()
    
    strk = data["starknet"]
    owb = data["owb"]
    
    msg = f"🕒 <b>Текущие цены</b>\n\n"
    msg += f"STRK: ${strk['usd']:.4f} ({strk.get('usd_24h_change',0):+.1f}%)\n"
    msg += f"OWB: ${owb['usd']:.4f} ({owb.get('usd_24h_change',0):+.1f}%)"
    
    await update.message.reply_text(msg, parse_mode='HTML')

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("price", price))
    print("Бот запущен. Напиши /price")
    app.run_polling()

if name == "main":
    main()
