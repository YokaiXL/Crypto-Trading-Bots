#FDV/MCAP oranı incelediğiniz coin ile ilgili size bir fikir sunar.FDV (Fully Diluted Valuation), bir kripto para biriminin toplam arzının,
#mevcut piyasa fiyatı ile çarpılmasıyla elde edilen değeri ifade eder. Bu, mevcut arzın yanı sıra, gelecekte madencilik,
#staking veya diğer yollarla piyasaya sürülecek tüm token veya coin'lerin toplam değerini gösterir. FDV, bir kripto varlığının potansiyel tam değerini değerlendirmek için kullanılır
#ve genellikle projenin büyüme ve gelişme potansiyelini anlamak isteyen yatırımcılar tarafından dikkate alınır.
#FDV/MCAP oranının maksimum 3 olması coine yatırım yapılması için olumlu bir fikir sunabilir.

#*Kodu çalıştırmadan önce request ve telegram-bot-python kütüphanelerini yüklemeyi unutmayın.
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# CoinMarketCap API bilgileri (CMC API anahtarınızı buraya girin)
CMC_API_KEY = "API KEY"
CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# BotFather'dan aldığınız bot token keyinizi buraya girin.
TELEGRAM_BOT_TOKEN = "BOT TOKEN KEY"

# FDV/MCAP oranını hesaplayan fonksiyonumuz.
def calculate_fdv_mcap(symbol):
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }
    params = {"symbol": symbol, "convert": "USD"}
    response = requests.get(CMC_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        coin_data = data["data"].get(symbol)
        if not coin_data:
            return "Geçersiz coin sembolü. Lütfen kontrol edin."

        mcap = coin_data["quote"]["USD"]["market_cap"]
        fdv = coin_data["quote"]["USD"]["fully_diluted_market_cap"]

        if mcap and fdv:
            ratio = fdv / mcap
            return (
                f"{coin_data['name']} ({symbol}):\n"
                f"Market Cap: ${mcap:,.2f}\n"
                f"Fully Diluted Valuation: ${fdv:,.2f}\n"
                f"FDV/MCAP Ratio: {ratio:.2f}"
            )
        else:
            return "Bu coin için yeterli veri bulunamadı."
    else:
        return f"API Hatası: {response.status_code}"

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Merhaba! Ben FDV/MCAP hesaplama botuyum. Bana bir coin sembolü göndererek FDV/MCAP oranını öğrenebilirsiniz.\n\n"
        "Örnekler:\n"
        "- BTC (Bitcoin)\n"
        "- ETH (Ethereum)\n\n"
        "Başlamak için bir coin sembolü girin!"
    )

# Kullanıcıdan coin sembolü al
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbol = update.message.text.upper()
    result = calculate_fdv_mcap(symbol)
    await update.message.reply_text(result)

# Telegram botunu başlatma
def main():
    # Telegram bot uygulamasını başlat
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Komutları ve mesajları işleyiciye bağlama
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botu çalıştır
    application.run_polling()

if __name__ == "__main__":
    main()
