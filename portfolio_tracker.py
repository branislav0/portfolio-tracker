#!/usr/bin/env python3
"""
Portfolio tracker using Finnhub API (better rate limits).
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime

# Configuration
FINNHUB_API_KEY = "d3mk91pr01qmso347l8gd3mk91pr01qmso347l90"
TELEGRAM_BOT_TOKEN = "BOTTOKENHERE"
TELEGRAM_CHAT_ID = "IDHERE"


def get_usd_to_eur_rate():
    """Get USD to EUR exchange rate."""
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        if 'rates' in data and 'EUR' in data['rates']:
            return float(data['rates']['EUR'])
        return 0.85  # Fallback rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return 0.85  # Fallback rate

def get_stock_price_finnhub(symbol):
    """Get stock price from Finnhub and convert to EUR."""
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        if 'c' in data and data['c']:  # 'c' is current price
            usd_price = float(data['c'])
            eur_rate = get_usd_to_eur_rate()
            return usd_price * eur_rate
        return None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def get_crypto_price(coin_id):
    """Get crypto price from CoinGecko."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=eur"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        if coin_id in data and 'eur' in data[coin_id]:
            return float(data[coin_id]['eur'])
        return None
    except Exception as e:
        print(f"Error fetching {coin_id}: {e}")
        return None

def send_telegram_message(message):
    """Send message via Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        post_data = urllib.parse.urlencode(data).encode()
        with urllib.request.urlopen(url, data=post_data) as response:
            result = json.loads(response.read().decode())
            return result.get('ok', False)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

def format_portfolio_message(portfolio_data):
    """Format portfolio data into message."""
    message = "📊 <b>Portfolio Update</b>\n\n"
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    message += f"🕐 <i>{timestamp}</i>\n\n"
    
    # Add holdings
    message += "📈 <b>Holdings:</b>\n"
    total_value = 0
    
    for symbol, data in portfolio_data.items():
        price = data.get('price', 0)
        quantity = data.get('quantity', 0)
        value = price * quantity if price else 0
        total_value += value
        
        if price:
            message += f"• {symbol}: €{price:.2f} × {quantity} = <b>€{value:.2f}</b>\n"
        else:
            message += f"• {symbol}: <i>Price unavailable</i> × {quantity}\n"
    
    # Add total value
    message += f"\n💰 <b>Total Portfolio Value: €{total_value:.2f}</b>\n"
    
    return message

def main():
    """Main function."""
    print("🚀 Starting Portfolio Tracker (Finnhub API)...")
    
    portfolio_data = {}
    total_value = 0
    
    # Fetch stock prices
    print("📈 Fetching stock prices...")
    stock_symbols = ["GOOGL", "NVDA", "META", "BABA", "AAPL", "WBD"]
    for symbol in stock_symbols:
        if symbol in HOLDINGS:
            price = get_stock_price_finnhub(symbol)
            quantity = HOLDINGS[symbol]
            value = price * quantity if price else 0
            total_value += value
            
            portfolio_data[symbol] = {
                'quantity': quantity,
                'price': price,
                'value': value
            }
            
            if price:
                print(f"  {symbol}: €{price:.2f} × {quantity} = €{value:.2f}")
            else:
                print(f"  {symbol}: Price unavailable")
    
    # Fetch crypto prices
    print("🪙 Fetching crypto prices...")
    crypto_mapping = {"BTC": "bitcoin", "ADA": "cardano"}
    
    for symbol in ["ADA"]:
        if symbol in HOLDINGS:
            coin_id = crypto_mapping[symbol]
            price = get_crypto_price(coin_id)
            quantity = HOLDINGS[symbol]
            value = price * quantity if price else 0
            total_value += value
            
            portfolio_data[symbol] = {
                'quantity': quantity,
                'price': price,
                'value': value
            }
            
            print(f"  {symbol}: €{price:.2f} × {quantity} = €{value:.2f}")
    
    print(f"\n💰 Total Portfolio Value: €{total_value:.2f}")
    
    # Format and send message
    message = format_portfolio_message(portfolio_data)
    print("\n📱 Sending Telegram message...")
    
    if send_telegram_message(message):
        print("✅ Portfolio update sent successfully!")
    else:
        print("❌ Failed to send portfolio update")

if __name__ == "__main__":
    main()
