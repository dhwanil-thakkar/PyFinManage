from typing_extensions import Self

from datetime import datetime

from yfinance_utils import get_current_price, get_stock_name

class Stock:
    def __init__(self, ticker_symbol: str):
        self.ticker_symbol: str = ticker_symbol
        self.name: str = get_stock_name(self.ticker_symbol)
        self.average_price_per_unit: float = 0
        self.number_of_stocks_owned: int = 0
        self.current_market_price: float = 0
        self.market_price_refresh_timestamp : datetime = datetime(1970,1,1)

    def register_stock_purchase(self, purchase_quantity, buying_price) -> Self:
        if(purchase_quantity <= 0):
            raise ValueError("Purchase Quantity must be positive")
        if (buying_price <=0):
            raise ValueError("Buying Price must be Positive")
        self.average_price_per_unit = ((self.average_price_per_unit * self.number_of_stocks_owned) + (purchase_quantity * buying_price)) / (self.number_of_stocks_owned + purchase_quantity)
        self.number_of_stocks_owned += purchase_quantity
        return self
    
    def register_stock_sell(self, selling_quantity, selling_price) -> Self:
        if(purchase_quantity <= 0):
            raise ValueError("Purchase Quantity must be positive")
        if (buying_price <=0):
            raise ValueError("Buying Price must be Positive")
        if (selling_quantity > self.number_of_stocks_owned):
            raise ValueError("Cannot Sell More that what you Own ")
        self.average_price_per_unit = ((self.average_price_per_unit * self.number_of_stocks_owned) - (selling_quantity * selling_price)) / (self.number_of_stocks_owned - selling_quantity)
        self.number_of_stocks_owned -= selling_quantity
        return self

    def refresh_current_price(self) -> Self :
        self.current_market_price = get_current_price(self.ticker_symbol)
        self.market_price_refresh_timestamp = datetime.now()
        return self
    

class Portfolio:
    def __init__(self, name: str):
        self.positions: dict[str, Stock] = {}

    def add_stock_to_portfolio(self, stock: Stock, purchase_quantity: float, buying_price: float) -> Self:
        print(f"Addding {purchase_quantity} of {stock.ticker_symbol} at {buying_price}")
        if (stock.ticker_symbol in  self.positions.keys()):
            print("This stock is already present")
        else:
            self.positions[stock.ticker_symbol] = stock
            print("New Stock Added")
        stock.register_stock_purchase(purchase_quantity=purchase_quantity, buying_price=buying_price)
        return self

    def get_positions(self):
        print(f"Name \t\t\t\tStocksOwned \tAveragePrice \tmarketPrice \tMarketpriceRefreshTimeStamp")
        for k,v in self.positions.items():
            v.refresh_current_price()
            print(f"{v.name} \t{v.number_of_stocks_owned} \t\t{v.average_price_per_unit} \t\t{v.current_market_price} \t\t{v.market_price_refresh_timestamp}")
        return self.positions.items()





portfolio_a = Portfolio("WelathSimplePortfolio")

microsoft_stock = Stock("MSFT")
apple_stock = Stock("AAPL")


portfolio_a.get_positions()

portfolio_a.add_stock_to_portfolio(stock = microsoft_stock, purchase_quantity=100, buying_price=50)
portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=50)
portfolio_a.get_positions()

portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=100)
portfolio_a.get_positions()

portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=200)
portfolio_a.get_positions()

