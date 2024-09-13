import yfinance as yf
 
from setup_logger import get_logger
logger = get_logger(__file__)

def get_current_price(ticker_symbol: str) -> float:

#    print(f"Geting current price for{ticker_symbol}")
    yfinance_current_price_key = "currentPrice"
    try:
        print(yf.Ticker(ticker_symbol).info[yfinance_current_price_key])
        return yf.Ticker(ticker_symbol).info[yfinance_current_price_key]
    except Exception as e:
        logger.error("Unbale to fetch price")
        return 0.0


def get_stock_name(ticker_symbol: str) -> str:
    yfinance_name_key = "longName"
    try:
        return yf.Ticker(ticker_symbol).info[yfinance_name_key]
    except Exception as e:
        logger.error("Unable to Fetch Name")
        return 0.0