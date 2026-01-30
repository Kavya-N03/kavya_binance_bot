# Binance Futures Trading Bot (CLI)

This is a command-line based Binance USDT-M Futures Trading Bot.  
It supports basic orders, advanced orders, validation, logging, and automated trading strategies.

---

## Features

###  Core Orders
- **Market Order**
- **Limit Order**

###  Advanced Orders
- **Stop-Limit Order**
- **OCO Order (One Cancels the Other)**
- **TWAP Strategy (Time-Weighted Average Price)**
- **Grid Trading Strategy**

###  Validation
- Symbol validation  
- Quantity validation  
- Price validation  

### Logging
All actions, errors, and responses are logged into:



## 📂 Installation & Setup

1. **Clone the repository**
   ```bash
   https://github.com/Kavya-N03/kavya_binance_bot.git
   cd kavya_binance_bot

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   
3. **Install Dependencies**
   ```bash
   pip install python-binance
   pip install python-dotenv
   pip install -r requirements.txt


4. **Create your .env file**
   ```bash
   BINANCE_API_KEY=your_api_key
   BINANCE_SECRET_KEY=your_secret_key








