# 📊 Portfolio Tracker

A Python application that tracks your portfolio prices (US stocks and cryptocurrencies) and sends updates via Telegram. Features both interactive Telegram bot commands and automated portfolio monitoring.

## ✨ Features

- 📈 **Real-time Stock Prices**: Fetches US stock prices using Finnhub API
- 🪙 **Cryptocurrency Tracking**: Fetches crypto prices using CoinGecko API
- 💶 **Euro Conversion**: All prices displayed in Euros with real-time exchange rates
- 📱 **Interactive Telegram Bot**: Manage your portfolio through Telegram chat commands
- 🔄 **Automated Updates**: Get portfolio updates on demand or schedule them
- ⚡ **High Rate Limits**: 60 calls/minute with Finnhub API (vs 5 with Alpha Vantage)
- 🛡️ **Error Handling**: Robust error handling and logging
- 📊 **Portfolio Calculation**: Automatic total value calculation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Telegram account
- API keys (see Configuration section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/branislav0/portfolio-tracker
   cd portfolio-tracker
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

3. **Run the interactive bot**
   ```bash
   python3 telegram_bot.py
   ```

4. **Go to Telegram and send `/start` to your bot**

## ⚙️ Configuration

### Required API Keys

#### 1. Finnhub API (Stocks)
- **Get it**: [Finnhub.io](https://finnhub.io/register)
- **Rate Limit**: 60 calls/minute (free tier)
- **Cost**: Free

#### 2. Telegram Bot
- **Create bot**: Message [@BotFather](https://t.me/botfather) on Telegram
- **Get chat ID**: Message [@userinfobot](https://t.me/userinfobot)
- **Cost**: Free

#### 3. CoinGecko API (Crypto)
- **Rate Limit**: 10-50 calls/minute
- **Cost**: Free (no API key required)

### Environment Variables

Create a `.env` file with your credentials:

```env
# Finnhub API Key (get from https://finnhub.io/register)
FINNHUB_API_KEY=your_finnhub_api_key_here

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

### Portfolio Configuration

Your portfolio is automatically initialized with sample holdings:
- **Stocks**: GOOGL, NVDA, META, BABA, AAPL, WBD
- **Crypto**: ADA (Cardano)

You can modify these through Telegram commands or by editing the `load_portfolio()` function in `telegram_bot.py`.

## 📱 Usage

### Interactive Telegram Bot

The bot runs continuously and responds to commands:

#### **Portfolio Management**
```
/start          # Show help and available commands
/list           # Show current portfolio
/add SYMBOL QTY # Add asset (e.g., /add BTC 0.1)
/remove SYMBOL  # Remove asset (e.g., /remove AAPL)
/clear          # Clear all assets
```

#### **Price Updates**
```
/update         # Get current portfolio value with live prices
```

#### **Examples**
```
/add BTC 0.1    # Add 0.1 Bitcoin
/add ETH 2      # Add 2 Ethereum
/remove WBD     # Remove Warner Bros Discovery
/update         # Get current prices
```

### One-time Portfolio Update

For a single portfolio update without the interactive bot:

```bash
python3 portfolio_tracker.py
```

## 🖼️ Screenshots

<!-- Add screenshots here -->
*Screenshots will be added showing:*
- *Telegram bot interface*
- *Portfolio update messages*
- *Command examples*

## 🚀 Deployment

### Local Background Execution

Run the bot in the background:

```bash
# Start bot in background
nohup python3 telegram_bot.py > bot.log 2>&1 &

# Check if running
ps aux | grep telegram_bot

# View logs
tail -f bot.log

# Stop bot
pkill -f telegram_bot.py
```

### GitHub Actions (Automated)

The project includes a GitHub Actions workflow for automated hourly updates:

1. **Push to GitHub**
2. **Add secrets** in repository settings:
   - `FINNHUB_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. **Workflow runs automatically** every hour

### Cron Job (Local Automation)

Set up hourly automation on your local machine:

```bash
# Edit crontab
crontab -e

# Add this line for hourly updates
0 * * * * cd /path/to/portfolio-tracker && python3 portfolio_tracker.py
```

## 📁 Project Structure

```
portfolio-tracker/
├── .env                    # Your API keys (DO NOT COMMIT)
├── .env.example            # Template for environment variables
├── .github/workflows/cron.yml  # GitHub Actions for automation
├── .gitignore              # Git ignore rules
├── portfolio_tracker.py    # One-time portfolio update script
├── telegram_bot.py         # Interactive Telegram bot
├── portfolio.json          # Portfolio data (auto-generated)
├── bot.log                 # Bot logs (auto-generated)
└── README.md               # This file
```

## 🔒 Security & Privacy

### .gitignore Recommendations

Add these to your `.gitignore` to protect sensitive information:

```gitignore
# Environment variables
.env

# Logs
*.log
bot.log

# Portfolio data
portfolio.json

# Python cache
__pycache__/
*.pyc
*.pyo

# OS files
.DS_Store
Thumbs.db
```

### Environment Variables Template

Use `.env.example` as a template:

```env
# Finnhub API Key (get from https://finnhub.io/register)
FINNHUB_API_KEY=your_finnhub_api_key_here

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

## 🛠️ Development

### Adding New Features

1. **New Stock Symbols**: Add to the `get_stock_price_finnhub()` function
2. **New Crypto**: Add to the `crypto_mapping` in `telegram_bot.py`
3. **New Commands**: Add to the `handle_command()` function

### Testing

Test individual components:

```bash
# Test stock prices
python3 -c "
from telegram_bot import get_stock_price_finnhub
print('AAPL:', get_stock_price_finnhub('AAPL'))
"

# Test crypto prices
python3 -c "
from telegram_bot import get_crypto_price
print('ADA:', get_crypto_price('cardano'))
"
```

## 📊 API Rate Limits

| API | Rate Limit | Daily Limit | Cost |
|-----|------------|-------------|------|
| Finnhub | 60 calls/minute | 3,600 calls/day | Free |
| CoinGecko | 10-50 calls/minute | No limit | Free |
| Telegram | No significant limits | - | Free |

## 🐛 Troubleshooting

### Common Issues

1. **"Price unavailable"**
   - Check API key validity
   - Verify symbol spelling
   - Check rate limits

2. **Telegram bot not responding**
   - Verify bot token and chat ID
   - Check if bot is running: `ps aux | grep telegram_bot`
   - Check logs: `tail -f bot.log`

3. **API rate limits**
   - Finnhub: 60 calls/minute
   - Wait before retrying
   - Consider upgrading to premium

### Testing API Keys

```bash
# Test Finnhub
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=YOUR_API_KEY"

# Test Telegram
curl "https://api.telegram.org/botYOUR_BOT_TOKEN/getMe"

# Test CoinGecko (no key needed)
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the logs in `bot.log`
- Test your API keys individually
- Ensure all environment variables are set correctly

---

**Happy portfolio tracking! 📈💰**
