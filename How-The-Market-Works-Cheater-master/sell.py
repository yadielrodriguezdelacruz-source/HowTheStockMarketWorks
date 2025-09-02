import requests
import yfinance as yf
import time
from bs4 import BeautifulSoup
import json
import os

# Start a session to maintain login
session = requests.Session()

# Login URL and credentials
login_url = "https://app.howthemarketworks.com/login"
login_data = {
    'username': 'MiBombocla',  # Your username
    'password': 'tybcyk-sumkoc-wIqqu1'  # Your password
}

# Log in to the site
def login():
    response = session.post(login_url, data=login_data)
    return response.ok

if login():
    print("Login successful!")

    # Trade URL and Order History URL
    trade_url = "https://app.howthemarketworks.com/trading/placeorder"
    order_history_url = "https://app.howthemarketworks.com/trading/orderhistory"
    account_balance_url = "https://app.howthemarketworks.com/account/balance"

    # Define thresholds for selling (e.g. sell if stock price drops below a certain threshold)
    minimum_sell_percentage = -5  # Example: sell if stock has dropped 5% or more

    # File for saving sold stocks and last run time
    state_file = 'trading_state.json'
    registro_file = r"C:\Users\yadie\Downloads\How-The-Market-Works-Cheater-master\registros_de_venta.txt"

    # List of stocks to check for selling (these would typically come from your portfolio)
    stock_to_sell_list = [
        "AMD", "GOOGL", "AAPL", "AMZN", "MSFT"  # Example stocks to sell (replace with actual owned stocks)
    ]

    # Function to get current stock data
    def get_stock_data(symbol):
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="2d")
            if len(hist) < 2:
                print(f"Not enough data for {symbol}")
                return None
            price = hist['Close'].iloc[0]
            previous_price = hist['Close'].iloc[1]
            change_percentage = ((price - previous_price) / previous_price) * 100
            return price, change_percentage
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    # Function to place a sell order
    def place_sell_order(symbol, price, change_percentage):
        try:
            # Assuming you're selling only 1 share for simplicity. Adjust as needed.
            trade_data = {
                'OrderSide': '2',  # Order Side: 2 for selling
                'Symbol': symbol,
                'Quantity': '1',
                'OrderType': '1',
                'Price': '0',
                'OrderExpiration': '1',
                'ExpirationDate': '',
                'SecurityType': 'Equities',
                'Exchange': 'US',
                'IsMarketOpen': 'True',
                'TournamentID': '0',
                'AccountID': '0',
                'CompanyName': '',
                'Currency': '0',
                'UnitPrice': '0',
                'QuantityType': 'Amount',
            }

            sell_response = session.post(trade_url, data=trade_data)

            if sell_response.ok:
                print(f"Successfully placed the order to sell 1 share of {symbol}.")
                with open(registro_file, 'a') as registro:
                    registro.write(f"Stock: {symbol}, Sell Price: ${price:.2f}, Change: {change_percentage:.2f}%\n")
            else:
                print(f"Failed to place the sell order for {symbol}.")
        except Exception as e:
            print(f"Error placing sell order for {symbol}: {e}")

    # Function to check and sell stocks with negative performance
    def check_and_sell_stocks():
        if not stock_to_sell_list:
            print("No stocks to check!")
            return

        for symbol in stock_to_sell_list:
            print(f"Checking {symbol}...")  # Added for clarity in output
            data = get_stock_data(symbol)
            if data:
                price, change = data
                print(f"{symbol}: ${price:.2f} with {change:.2f}% change")

                if change <= minimum_sell_percentage:
                    print(f"Selling {symbol} as it has a {change:.2f}% drop and meets criteria.")
                    place_sell_order(symbol, price, change)
                else:
                    print(f"Skipping {symbol} due to insufficient drop in price.")
            else:
                print(f"Could not fetch data for {symbol}.")

    # Run the script once (removed the 1-hour wait time)
    print("\nChecking stocks and placing sell orders...")
    check_and_sell_stocks()

else:
    print("Login failed.")


