from fastapi import FastAPI, HTTPException, Depends
from db_models import SessionLocal, DB_Investment, DB_Portfolio
#from portfolioManager import Portfolio, Stock

from pydantic import BaseModel
from typing import Literal
from enum import Enum

from portfolioCrud import get_all_portfolios, get_portfolio, create_new_portfolio

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='api.log', encoding='utf-8', level=logging.DEBUG)

app = FastAPI()


class ActionType(Enum):
    buy = 'buy'
    sell = 'sell'

class StockTransactionDetails(BaseModel):
    ticker_symbol: str
    quantity: float
    price: float
    action: ActionType


# Endpoint to Create a new portfolio
@app.post("/create-new-portfolio/")
def create_portfolio(name: str):
    try:
        result = create_new_portfolio(name=name)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/portfolio/{name}")
def fetch_portfolio_details(name: str):
    try:
        portfolio = get_portfolio(name=name)
        return {"PorfolioDetails": portfolio}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get-all-portfolios/")
def get_portfolios(limit: int = 50):
    try:
        portfolios = get_all_portfolios(limit = limit)
        logger.debug(f"portfolios : {portfolios}")
        return {"portfolios": portfolios}
    except Exception as e:
        logging.error(f" Exception occuren in get-all-portfolios: {e}")
        raise HTTPException(status_code=400,detail=str(e))

@app.get("/portfolio/{name}/holdings")
def get_portfolio_holdings(name: str):
    try:
        db_portfolio = Portfolio.get_portfolio(name=name)
        portfolio = Portfolio(name=db_portfolio.name)
        holdings = portfolio.get_positions()
        return holdings
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@app.post("/portfolio/{portfolio_name}/transaction")
def add_or_remove_stock_to_portfolio(portfolio_name:str, transactionDetails: StockTransactionDetails):
    try:
        db_portfolio = Portfolio.get_portfolio(name=portfolio_name)
        portfolio = Portfolio(name=db_portfolio.name)
        if transactionDetails.action == ActionType.buy:
            portfolio.buy_stock_to_portfolio(ticker_symbol=transactionDetails.ticker_symbol, purchase_quantity = transactionDetails.quantity, buying_price = transactionDetails.price)
            return {"message": f"Stock updated in portfolio"}
        elif transactionDetails.action == ActionType.sell:
            portfolio.sell_stock_from_portfolio(stock=stock, selling_quantity=transactionDetails.quantity, selling_price=transactionDetails.price)
            return {"message": f"Stock updated in portfolio"}
        else:
            raise HTTPException(status_code=404, detail="Invalid Action")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        


# def get_portfolio_holdings():
# def add_a_stock_to_a_portfolio
# def remove a stock from a portfolio

