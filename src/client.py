from binance.client import Client
from dotenv import load_dotenv
import os

class BinanceClient:
    def __init__(self):
        load_dotenv()  # Load all values from the .env file
        
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_SECRET_KEY")

        # Validate both API keys
        if not api_key or not api_secret:
            raise ValueError("API Key or Secret Key not found in .env file")

        # Initialize Binance futures client (testnet)
        self.client = Client(api_key, api_secret, testnet=True)

    def get_client(self):
        return self.client
