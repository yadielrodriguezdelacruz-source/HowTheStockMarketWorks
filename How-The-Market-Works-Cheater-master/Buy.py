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
    'username': '',  # Your username
    'password': ''  # Your password
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

    # Define thresholds
    minimum_upside_threshold = 2  # Only buy if the upside is above this threshold

    # File for saving bought stocks and last run time
    state_file = 'trading_state.json'
    registro_file = r"C:\Users\yadie\Downloads\How-The-Market-Works-Cheater-master\registros_de_compra.txt"

    # Full list of S&P 500 symbols
    popular_stock_list = [
        "MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A", "APD", "ABNB", "AKAM", "ALB", "ARE", "ALGN",
        "ALLE", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AMCR", "AEE", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "AME",
        "AMGN", "APH", "ADI", "AON", "APA", "ACGL", "ADM", "ANET", "AJG", "AIZ", "T", "ATO", "ADSK", "ADP", "AZO", "AVB", "AVY",
        "AXON", "BKR", "BALL", "BAC", "BAX", "BDX", "BRK.B", "BBY", "TECH", "BIIB", "BLK", "BX", "XYZ", "BK", "BA", "BKNG", "BSX",
        "BMY", "AVGO", "BR", "BRO", "BF.B", "BLDR", "BG", "BXP", "CHRW", "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", "KMX", "CCL",
        "CARR", "CAT", "CBOE", "CBRE", "CDW", "COR", "CNC", "CNP", "CF", "CRL", "SCHW", "CHTR", "CVX", "CMG", "CB", "CHD", "CI",
        "CINF", "CTAS", "CSCO", "C", "CFG", "CLX", "CME", "CMS", "KO", "CTSH", "COIN", "CL", "CMCSA", "CAG", "COP", "ED", "STZ",
        "CEG", "COO", "CPRT", "GLW", "CPAY", "CTVA", "CSGP", "COST", "CTRA", "CRWD", "CCI", "CSX", "CMI", "CVS", "DHR", "DRI", "DDOG",
        "DVA", "DAY", "DECK", "DE", "DELL", "DAL", "DVN", "DXCM", "FANG", "DLR", "DG", "DLTR", "D", "DPZ", "DASH", "DOV", "DOW",
        "DHI", "DTE", "DUK", "DD", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV", "EMR", "ENPH", "ETR", "EOG", "EPAM", "EQT",
        "EFX", "EQIX", "EQR", "ERIE", "ESS", "EL", "EG", "EVRG", "ES", "EXC", "EXE", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FDS",
        "FICO", "FAST", "FRT", "FDX", "FIS", "FITB", "FSLR", "FE", "FI", "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN",
        "IT", "GE", "GEHC", "GEV", "GEN", "GNRC", "GD", "GIS", "GM", "GPC", "GILD", "GPN", "GL", "GDDY", "GS", "HAL", "HIG", "HAS",
        "HCA", "DOC", "HSIC", "HSY", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUBB", "HUM", "HBAN", "HII",
        "IBM", "IEX", "IDXX", "ITW", "INCY", "IR", "PODD", "INTC", "IBKR", "ICE", "IFF", "IP", "IPG", "INTU", "ISRG", "IVZ", "INVH",
        "IQV", "IRM", "JBHT", "JBL", "JKHY", "J", "JNJ", "JCI", "JPM", "K", "KVUE", "KDP", "KEY", "KEYS", "KMB", "KIM", "KMI", "KKR",
        "KLAC", "KHC", "KR", "LHX", "LH", "LRCX", "LW", "LVS", "LDOS", "LEN", "LII", "LLY", "LIN", "LYV", "LKQ", "LMT", "L", "LOW",
        "LULU", "LYB", "MTB", "MPC", "MKTX", "MAR", "MMC", "MLM", "MAS", "MA", "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET", "MTD",
        "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", "TAP", "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI",
        "NDAQ", "NTAP", "NFLX", "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN", "NSC", "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA",
        "NVR", "NXPI", "ORLY", "OXY", "ODFL", "OMC", "ON", "OKE", "ORCL", "OTIS", "PCAR", "PKG", "PLTR", "PANW", "PSKY", "PH", "PAYX",
        "PAYC", "PYPL", "PNR", "PEP", "PFE", "PCG", "PM", "PSX", "PNW", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU",
        "PEG", "PTC", "PSA", "PHM", "PWR", "QCOM", "DGX", "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RVTY", "ROK",
        "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SRE", "NOW", "SHW", "SPG", "SWKS", "SJM", "SW", "SNA", "SOLV",
        "SO", "LUV", "SWK", "SBUX", "STT", "STLD", "STE", "SYK", "SMCI", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TRGP",
        "TGT", "TEL", "TDY", "TER", "TSLA", "TXN", "TPL", "TXT", "TMO", "TJX", "TKO", "TTD", "TSCO", "TT", "TDG", "TRV", "TRMB", "TFC",
        "TYL", "TSN", "USB", "UBER", "UDR", "ULTA", "UNP", "UAL", "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VLTO", "VRSN", "VRSK",
        "VZ", "VRTX", "VTRS", "VICI", "V", "VST", "VMC", "WRB", "GWW", "WAB", "WMT", "DIS", "WBD", "WM", "WAT", "WEC", "WFC", "WELL",
        "WST", "WDC", "WY", "WSM", "WMB", "WTW", "WDAY", "WYNN", "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZTS"
    ]

    # Function to get current stock data
    def get_stock_data(symbol):
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="60d")  # Fetch last 60 days of data
            if len(hist) < 50:
                print(f"Not enough data for {symbol}")
                return None

            # Get the current price
            current_price = hist['Close'].iloc[-1]

            # Get the average price over the last 50 days (or use a longer period for a smoother average)
            avg_price = hist['Close'].iloc[-50:].mean()

            # Calculate the price difference percentage
            price_diff_percentage = ((current_price - avg_price) / avg_price) * 100

            return current_price, avg_price, price_diff_percentage
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    # Function to get account balance (using the fixed balance)
    def get_account_balance():
        available_balance = 2999.74  # Fixed balance
        print(f"Available balance: ${available_balance:.2f}")
        return available_balance

    # Function to place a buy order
    def place_buy_order(symbol, price, change_percentage):
        try:
            available_balance = get_account_balance()

            if price > available_balance:
                print(f"Not enough balance to buy {symbol} at ${price:.2f}. Skipping.")
                return

            trade_data = {
                'OrderSide': '1',
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

            trade_response = session.post(trade_url, data=trade_data)

            if trade_response.ok:
                print(f"Successfully placed the order to buy 1 share of {symbol}.")
                with open(registro_file, 'a') as registro:
                    registro.write(f"Stock: {symbol}, Buy Price: ${price:.2f}, Price Difference: {change_percentage:.2f}%\n")
            else:
                print(f"Failed to place the buy order for {symbol}.")
        except Exception as e:
            print(f"Error placing buy order for {symbol}: {e}")

    # Function to check and buy stocks when their price is below their average price
    def check_and_buy_stocks():
        if not popular_stock_list:
            print("No stocks to check!")
            return

        for symbol in popular_stock_list:
            print(f"Checking {symbol}...")  # Added for clarity in output
            data = get_stock_data(symbol)
            if data:
                current_price, avg_price, price_diff = data
                print(f"{symbol}: Current Price: ${current_price:.2f}, Average Price: ${avg_price:.2f}, Price Difference: {price_diff:.2f}%")

                if price_diff <= -10:  # Buy if the current price is 10% lower than the average price
                    print(f"Buying {symbol} as it is 10% lower than its average price and meets criteria.")
                    place_buy_order(symbol, current_price, price_diff)
                else:
                    print(f"Skipping {symbol} due to insufficient drop in price.")
            else:
                print(f"Could not fetch data for {symbol}.")

    # Run the script once (removed the 1-hour wait time)
    print("\nChecking stocks and placing buy orders...")
    check_and_buy_stocks()

else:
    print("Login failed.")
