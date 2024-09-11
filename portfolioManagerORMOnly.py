from typing_extensions import Self

from db_models import DB_Investment, DB_Portfolio, SessionLocal
from datetime import datetime
from yfinance_utils import get_current_price, get_stock_name





class Stock(DB_Investment):
    # def __init__(self, ticker_symbol: str, name: str = None, average_price_per_unit: float = 0,number_of_stocks_owned:float = 0, current_market_price: float = 0, market_price_refresh_timestamp: datetime = datetime(1970,1,1)):
    #     self.ticker_symbol: str = ticker_symbol
    #     self.name: str = get_stock_name(self.ticker_symbol)
    #     self.average_price_per_unit: float = average_price_per_unit
    #     self.number_of_stocks_owned: int = number_of_stocks_owned
    #     self.current_market_price: float = current_market_price
    #     self.market_price_refresh_timestamp : datetime = market_price_refresh_timestamp

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

    def convert_to_db_investment(self, portfolio_id: int) -> DB_Investment:
        return DB_Investment(
            ticker_symbol = self.ticker_symbol,
            name = self.name,
            average_price_per_unit = self.average_price_per_unit,
            number_of_stocks_owned = self.number_of_stocks_owned,
            current_market_price = self.current_market_price,
            market_price_refresh_timestamp = self.market_price_refresh_timestamp,
            portfolio_id=portfolio_id
        )

    @staticmethod
    def convert_to_domain_stock(db_stock: DB_Investment):
        return Stock(
            ticker_symbol=db_stock.ticker_symbol,
            name=db_stock.name,
            average_price_per_unit=db_stock.average_price_per_unit,
            number_of_stocks_owned=db_stock.number_of_stocks_owned,
            current_market_price=db_stock.current_market_price,
            market_price_refresh_timestamp=db_stock.market_price_refresh_timestamp
        )

    @staticmethod
    def get_stock_object(portfolio_name: str, ticker_symbol: str) :
        
        db_portfolio = Portfolio.get_portfolio(name=portfolio_name)
        with SessionLocal() as session:
            db_stock = session.query(DB_Investment).filter_by(portfolio_id = db_portfolio.portfolio_id, ticker_symbol=ticker_symbol).first()
            if not db_stock:
                stock = Stock(ticker_symbol=ticker_symbol)
                return stock
                # raise ValueError("stock investment in the portfolio does not exsist")
            stock = Stock.convert_to_domain_stock(db_stock)
            return stock


    
class Portfolio:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def create_new_portfolio(name:str):
        with SessionLocal() as session:
            portfolio = session.query(DB_Portfolio).filter_by(name=name).first()
            if portfolio:
                raise ValueError("Portfolio with the same name Already Exists")
            new_portfolio = DB_Portfolio(name=name)
            session.add(new_portfolio)
            session.commit()
            return {"message":f"Protfolio '{name}' created successfully"}

    @staticmethod
    def get_portfolio(name: str):
        with SessionLocal() as session:
            db_portfolio = session.query(DB_Portfolio).filter_by(name=name).first()
            if not db_portfolio:
                raise ValueError("Portfolio Does not exists")
            return db_portfolio   #Return an object of Portfolio 

    def buy_stock_to_portfolio(self, ticker_symbol: str, purchase_quantity: float, buying_price: float) -> Self:
        print(f"Addding {purchase_quantity} of {ticker_symbol} at {buying_price} in portfolio {self.name}")
        db_portfolio = Portfolio.get_portfolio(self.name)
        with SessionLocal() as session:
            stock = Stock.get_stock_object(portfolio_name=self.name, ticker_symbol=ticker_symbol)
            stock.register_stock_purchase(purchase_quantity=purchase_quantity, buying_price=buying_price)
            stock.refresh_current_price()
            db_stock = stock.convert_to_db_investment(portfolio_id = db_portfolio.portfolio_id)
            session.add(db_stock)
            session.commit()
        #stock.save_to_db(stock)

        print("New Stock Added")
        return self

    def sell_stock_from_portfolio(self, stock: Stock, selling_quantity: float, selling_price: float) -> Self:
        print(f"selling {purchase_quantity} of {stock.ticker_symbol} at {buying_price} from portfolio {self.name}")

        stock.register_stock_sell(selling_quantity=selling_quantity, selling_price=selling_price)
        stock.refresh_current_price()
        stock.save_to_db(stock)

        print("Stocks sold")
        return self


    def get_positions(self):
        with SessionLocal() as session:
            portfolio = session.query(DB_Portfolio).filter_by(name=self.name).first()
            if not portfolio:
                print("Portfolio not found.")
                raise ValueError("Portfolio does not exsists")
            if portfolio:
                investments = session.query(DB_Investment).filter_by(portfolio_id=portfolio.portfolio_id).all()


### This will print the postions to the console using tabulate
                # headers = ["Name","Stocks Owned","Average Price", "Market Price", "Market Price RefreshnTimestamp"]
                # rows = [[inv.name ,  inv.number_of_stocks_owned, inv.average_price_per_unit, inv.current_market_price, inv.market_price_refresh_timestamp]
                #     for inv in investments]
                
                # # Display using tabulate
                # print(f"\n Portfolio: {portfolio.name}\n")
                # print(tabulate(rows, headers=headers, tablefmt="grid"))

                positions= {
                    "PortfolioName": portfolio.name,
                    "Portfolio_ID": portfolio.portfolio_id,
                    "holdings": [
                        {
                            "name": inv.name,
                            "number_of_stocks_owned": inv.number_of_stocks_owned,
                            "average_price_per_unit": inv.average_price_per_unit,
                            "current_market_price": inv.current_market_price,
                            "market_price_refresh_timestamp": inv.market_price_refresh_timestamp.isoformat()  # Convert datetime to ISO format
                        }
                        for inv in investments
                    ]
                }
                return positions
            else:
                print("Could not get positions")
                raise Exception("Error getting positions")



