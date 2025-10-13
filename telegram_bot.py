#!/usr/bin/env python3
"""
Interactive Telegram bot for portfolio management.
Allows you to configure assets through Telegram chat commands.
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime
import time
import os

# Configuration
FINNHUB_API_KEY = "d3mk91pr01qmso347l8gd3mk91pr01qmso347l90"
TELEGRAM_BOT_TOKEN = "BOTTOKENHERE"
TELEGRAM_CHAT_ID = "TOKENHERE"

# Portfolio storage
PORTFOLIO_FILE = "portfolio.json"

def load_portfolio():
    """Load portfolio from file."""
    try:
        with open(PORTFOLIO_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:

        default_portfolio = {
        }
        save_portfolio(default_portfolio)
        return default_portfolio

def save_portfolio(portfolio):
    """Save portfolio to file."""
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=2)

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

def get_updates(offset=None):
    """Get updates from Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
        params = {}
        if offset:
            params['offset'] = offset
        
        if params:
            url += "?" + urllib.parse.urlencode(params)
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get('result', [])
    except Exception as e:
        print(f"Error getting updates: {e}")
        return []

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

def process_portfolio_update():
    """Process portfolio and send update."""
    portfolio = load_portfolio()
    portfolio_data = {}
    total_value = 0
    
    # Crypto mapping
    crypto_mapping = {"BTC": "bitcoin", "ADA": "cardano", "ETH": "ethereum"}
    
    for symbol, quantity in portfolio.items():
        price = None
        
        # Check if it's crypto
        if symbol in crypto_mapping:
            price = get_crypto_price(crypto_mapping[symbol])
        else:
            # Assume it's a stock
            price = get_stock_price_finnhub(symbol)
        
        if price:
            value = price * quantity
            total_value += value
            portfolio_data[symbol] = {
                'quantity': quantity,
                'price': price,
                'value': value
            }
        else:
            portfolio_data[symbol] = {
                'quantity': quantity,
                'price': None,
                'value': 0
            }
    
    message = format_portfolio_message(portfolio_data)
    send_telegram_message(message)
    return portfolio_data

def handle_command(command, text):
    """Handle Telegram commands."""
    text = text.strip()
    
    if command == "/start":
        help_message = """
🤖 <b>Portfolio Tracker Bot</b>

<b>Commands:</b>
/add [SYMBOL] [QUANTITY] - Add asset to portfolio
/remove [SYMBOL] - Remove asset from portfolio
/list - Show current portfolio
/update - Get portfolio update with current prices
/clear - Clear all assets
/help - Show this help

<b>Examples:</b>
/add AAPL 2.5
/add BTC 0.1
/add ADA 1000
/remove AAPL
/list
/update
        """
        send_telegram_message(help_message)
    
    elif command == "/add":
        parts = text.split()
        if len(parts) >= 2:
            symbol = parts[0].upper()
            try:
                quantity = float(parts[1])
                portfolio = load_portfolio()
                portfolio[symbol] = quantity
                save_portfolio(portfolio)
                send_telegram_message(f"✅ Added {symbol}: {quantity} to portfolio")
            except ValueError:
                send_telegram_message("❌ Invalid quantity. Use: /add SYMBOL QUANTITY")
        else:
            send_telegram_message("❌ Usage: /add SYMBOL QUANTITY")
    
    elif command == "/remove":
        symbol = text.upper()
        portfolio = load_portfolio()
        if symbol in portfolio:
            del portfolio[symbol]
            save_portfolio(portfolio)
            send_telegram_message(f"✅ Removed {symbol} from portfolio")
        else:
            send_telegram_message(f"❌ {symbol} not found in portfolio")
    
    elif command == "/list":
        portfolio = load_portfolio()
        if portfolio:
            message = "📋 <b>Current Portfolio:</b>\n\n"
            for symbol, quantity in portfolio.items():
                message += f"• {symbol}: {quantity}\n"
            send_telegram_message(message)
        else:
            send_telegram_message("📋 Portfolio is empty")
    
    elif command == "/update":
        send_telegram_message("🔄 Fetching latest prices...")
        process_portfolio_update()
    
    elif command == "/clear":
        save_portfolio({})
        send_telegram_message("🗑️ Portfolio cleared")
    
    elif command == "/help":
        handle_command("/start", "")
    
    else:
        send_telegram_message("❌ Unknown command. Use /help for available commands")

def main():
    """Main bot loop."""
    print("🤖 Starting Portfolio Tracker Bot...")
    print("Send /start to your bot to begin!")
    
    last_update_id = 0
    
    while True:
        try:
            updates = get_updates(last_update_id + 1)
            
            for update in updates:
                last_update_id = update['update_id']
                
                if 'message' in update and 'text' in update['message']:
                    message = update['message']
                    text = message['text']
                    
                    # Check if it's a command
                    if text.startswith('/'):
                        command = text.split()[0]
                        command_text = text[len(command):].strip()
                        print(f"Received command: {command} {command_text}")
                        handle_command(command, command_text)
                    else:
                        send_telegram_message("❓ Use /help to see available commands")
            
            time.sleep(1)  # Check for updates every second
            
        except KeyboardInterrupt:
            print("\n👋 Bot stopped")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
