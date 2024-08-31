import yfinance as yp
from typing_extensions import Self

class Stock:
    def __init__(self, ticker_symbol: str):
        self.ticker_Symbol: string = ticker_symbol
        self.average_price_per_stock: int = 0
        self.number_of_stocks_owned: int = 0
        self.current_price_of_stock: int = 0


    def register_stock_purchase(self, purchase_quantity, buying_price) -> Self:

        self.average_price_per_stock = ((self.average_price_per_stock * self.number_of_stocks_owned) + (purchase_quantity * buying_price)) / (self.number_of_stocks_owned + purchase_quantity)
        self.number_of_stocks_owned += purchase_quantity
        return self
    
    def register_stock_sell(self, selling_quantity, selling_price) -> Self:
        self.average_price_per_stock = ((self.average_price_per_stock * self.number_of_stocks_owned) - (selling_quantity * selling_price)) / (self.number_of_stocks_owned - selling_quantity)
        self.number_of_stocks_owned -= selling_quantity
        return self

    

class Portfolio:
    def __init__(self, name: str):
        self.positions: dict[str, Stock] = {}

    def add_stock_to_portfolio(self, stock: Stock, purchase_quantity: float, buying_price: float) -> Self:
        print(f"Addding {purchase_quantity} of {stock.ticker_Symbol} at {buying_price}")
        if (stock.ticker_Symbol in  self.positions.keys()):
            print("This stock is already present")
        else:
            self.positions[stock.ticker_Symbol] = stock
            print("New Stock Added")
        stock.register_stock_purchase(purchase_quantity=purchase_quantity, buying_price=buying_price)
        return self

    def get_positions(self):
        print(f"Name \tStocksOwned \tAveragePrice \tCurrentPrice")
        for k,v in self.positions.items():
            print(f"{k} \t{v.number_of_stocks_owned} \t\t{v.average_price_per_stock} \t\t{v.current_price_of_stock}")
        return self.positions.items()





portfolio_a = Portfolio("WelathSimplePortfolio")

microsoft_stock = Stock("MSFT")
apple_stock = Stock("APPL")


portfolio_a.get_positions()

portfolio_a.add_stock_to_portfolio(stock = microsoft_stock, purchase_quantity=100, buying_price=50)
portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=50)
portfolio_a.get_positions()

portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=100)
portfolio_a.get_positions()

portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=200)
portfolio_a.get_positions()

