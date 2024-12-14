#Bu bot ile günün en çok yükselen 3 coinini tek mesajda görebileceksiniz.

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Buraya CoinMarketCap API anahtarınızı girin
API_KEY = 'API KEY'

# CoinMarketCap'ten verileri alacak fonksiyon
def get_top_3_cryptos():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY,
        'Accept': 'application/json',
    }
    params = {
        'limit': 10,  # İlk 10 coin
        'sort': 'percent_change_24h',  # 24 saatlik değişim oranına göre sırala
        'convert': 'USD',  # USD cinsinden fiyat
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # İlk 3 coin'i al
    top_3 = []
    for coin in data['data'][:3]:
        name = coin['name']
        symbol = coin['symbol']
        price = coin['quote']['USD']['price']
        change_24h = coin['quote']['USD']['percent_change_24h']
        top_3.append(f"{name} ({symbol}): ${price:.2f} (+{change_24h:.2f}%)")

    return "\n".join(top_3)

# /top3 komutu için handler
async def top3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # CoinMarketCap verilerini al
    top_3 = get_top_3_cryptos()
    
    # Kullanıcıya yanıt gönder
    await update.message.reply_text(f"Bugünün en çok yükselen ilk 3 coini:\n{top_3}")

# Botu başlatan fonksiyon
def main():
    # Telegram Bot API Token'ınızı girin
    bot_token = 'bot tokeniniz'
    
    # Application'ı oluştur
    application = Application.builder().token(bot_token).build()

    # /top3 komutunu işleyen handler'ı ekle
    application.add_handler(CommandHandler("top3", top3))

    # Botu başlat
    application.run_polling()

if __name__ == '__main__':
    main()
