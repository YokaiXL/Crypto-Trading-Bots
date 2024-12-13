import requests

# CoinMarketCap API bilgileri
API_KEY = "d6c50878-25a1-499e-86b5-eb728360ef6c"
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# Kullanıcıdan coinin sembolünü al
symbol = input("Lütfen bir coinin sembolünü girin: ").upper()

# Header'lar ve parametreler
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,
}
parameters = {
    "symbol": symbol,
    "convert": "USD"  # Veriler USD cinsinden olacak
}

# API isteği gönder
try:
    response = requests.get(URL, headers=headers, params=parameters)
    response.raise_for_status()
    data = response.json()

    # Coin verilerini al
    coin_data = data['data'][symbol]
    mcap = coin_data['quote']['USD']['market_cap']
    fdv = coin_data['quote']['USD']['fully_diluted_market_cap']

    # FDV/MCAP oranını hesapla
    if mcap and fdv:
        fdv_mcap_ratio = fdv / mcap
        print(f"\n{coin_data['name']} ({symbol}):")
        print(f"Market Cap (MCAP): ${mcap:,.2f}")
        print(f"Fully Diluted Valuation (FDV): ${fdv:,.2f}")
        print(f"FDV/MCAP Oranı: {fdv_mcap_ratio:.2f}")
    else:
        print("Bu coin için yeterli veri bulunamadı.")

except requests.exceptions.RequestException as e:
    print("Bir hata oluştu:", e)
