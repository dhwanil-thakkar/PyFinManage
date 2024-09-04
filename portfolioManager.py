from typing_extensions import Self

from db_models import DB_Investment, DB_Portfolio, SessionLocal
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

    def save_to_db(self, portfolio_id: int) -> Self :
        with SessionLocal() as session:
            investment = session.query(DB_Investment).filter_by(ticker_symbol=self.ticker_symbol, portfolio_id = portfolio_id).first()
            if investment:
            # if the record already existss do something here
                investment.average_price_per_unit = self.average_price_per_unit
                investment.number_of_stocks_owned = self.number_of_stocks_owned
                investment.current_market_price = self.current_market_price
                investment.market_price_refresh_timestamp = self.market_price_refresh_timestamp
                
            else:
            # if the record does not exsit create a new record
                investment = DB_Investment(
                    ticker_symbol=self.ticker_symbol,
                    name = self.name,
                    average_price_per_unit = self.average_price_per_unit,
                    number_of_stocks_owned = self.number_of_stocks_owned,
                    current_market_price = self.current_market_price,
                    market_price_refresh_timestamp = self.market_price_refresh_timestamp,
                    portfolio_id = portfolio_id
                )
                session.add(investment)
            
            session.commit()

    

class Portfolio:
    def __init__(self, name: str):
        self.name = name
        
    def save_stock_to_db(self, stock: Stock):
        with SessionLocal() as session:
            portfolio = session.query(DB_Portfolio).filter_by(name=self.name).first()
        if not portfolio:
        # Create a entry for the Portfolio if it not already exsists
            portfolio = DB_Portfolio(name=self.name)
            session.add(portfolio)
            session.commit()
        stock.save_to_db(portfolio_id=portfolio.portfolio_id)

        

    def add_stock_to_portfolio(self, stock: Stock, purchase_quantity: float, buying_price: float) -> Self:
        print(f"Addding {purchase_quantity} of {stock.ticker_symbol} at {buying_price}")
            
        stock.register_stock_purchase(purchase_quantity=purchase_quantity, buying_price=buying_price)
        stock.refresh_current_price()
        self.save_stock_to_db(stock)

        print("New Stock Added")
        return self

    def get_positions(self):
        with SessionLocal() as session:
            portfolio = session.query(DB_Portfolio).filter_by(name=self.name).first()
            if portfolio:
                investments = session.query(DB_Investment).filter_by(portfolio_id=portfolio.portfolio_id).all()
                print(f"Name \t\t\t\tStocksOwned \tAveragePrice \tMarketPrice \tMarketPriceRefreshTimestamp")
                for inv in investments:
                    print(f"{inv.name} \t{inv.number_of_stocks_owned} \t\t{inv.average_price_per_unit} \t\t{inv.current_market_price} \t\t{inv.market_price_refresh_timestamp}")
            else:
                print("Portfolio not found.")



portfolio_a = Portfolio("WelathSimplePortfolio")

microsoft_stock = Stock("MSFT")
apple_stock = Stock("AAPL")


portfolio_a.get_positions()

portfolio_a.add_stock_to_portfolio(stock = microsoft_stock, purchase_quantity=100, buying_price=50)
portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=50)

portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=100)

portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=200)
portfolio_a.get_positions()


portfolio_b = Portfolio("2nd Portfolio")

portfolio_b.get_positions()

portfolio_b.add_stock_to_portfolio(stock = microsoft_stock, purchase_quantity=100, buying_price=50)
portfolio_b.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=50)

portfolio_b.get_positions()

