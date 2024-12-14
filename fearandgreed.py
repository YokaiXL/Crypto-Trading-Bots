import requests
from telegram import Bot
from telegram.ext import Application, CommandHandler

# CoinMarketCap API anahtarınızı buraya ekleyin
API_KEY = 'API KEY'
CMC_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/market-pair/v1'

# Telegram Bot Token'ınızı buraya ekleyin
TELEGRAM_TOKEN = 'BOT TOKEN KEY'

# CoinMarketCap'ten korku/açgözlülük endeksini almak için bir fonksiyon
def get_fear_greed_index():
    url = 'https://api.alternative.me/fng/'
    response = requests.get(url)
    data = response.json()
    fear_greed_index = data['data'][0]['value']
    return fear_greed_index

# Telegram botunda "/fear" komutuna yanıt
async def fear(update, context):
    fear_greed_index = get_fear_greed_index()
    await update.message.reply_text(f"Korku/Açgözlülük Endeksi: {fear_greed_index}")

# Telegram botunu başlatan fonksiyon
def start_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("fear", fear))  # /fear komutu
    application.run_polling()

if __name__ == '__main__':
    start_bot()
