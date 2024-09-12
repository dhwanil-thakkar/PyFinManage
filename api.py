from fastapi import FastAPI, HTTPException, Depends
from db_models import SessionLocal, DB_Investment, DB_Portfolio
#from portfolioManager import Portfolio, Stock

from validatonModels import StockTransactionDetails, ActionType
from portfolioCrud import get_all_portfolios, create_new_portfolio, get_all_investments
from investmentCrud import buy_investment_to_portfolio, sell_investment_from_portfolio


from setup_logger import get_logger

logger = get_logger(__file__)



app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Endpoint to Create a new portfolio
@app.post("/create-new-portfolio/")
def create_portfolio(name: str, db: SessionLocal = Depends(get_db)):
    try:
        result = create_new_portfolio(name=name, db=db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/portfolio/{name}")
def fetch_portfolio_details(name: str, db: SessionLocal = Depends(get_db)):
    try:
        portfolio = get_portfolio(name=name)
        return {"PorfolioDetails": portfolio}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get-all-portfolios/")
def get_portfolios(limit: int = 50, db: SessionLocal = Depends(get_db)):
    try:
        portfolios = get_all_portfolios(limit = limit, db=db)
        logger.debug(f"portfolios : {portfolios}")
        return {"portfolios": portfolios}
    except Exception as e:
        logging.error(f" Exception occuren in get-all-portfolios: {e}")
        raise HTTPException(status_code=400,detail=str(e))

@app.get("/portfolio/{name}/investments")
def get_portfolio_investements(name: str, limit: int = 50, db: SessionLocal = Depends(get_db)):
    try:
        holdings = get_all_investments(portfolio_name=name, limit=limit, db=db)
        return {"holdings":holdings}
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@app.post("/portfolio/{portfolio_name}/transaction")
def add_or_remove_stock_to_portfolio(portfolio_name:str, transactionDetails: StockTransactionDetails, db: SessionLocal = Depends(get_db)):
    try:
#        db_portfolio = Portfolio.get_portfolio(name=portfolio_name)
#        portfolio = Portfolio(name=db_portfolio.name)
        logger.debug(transactionDetails)
        if transactionDetails.action == ActionType.buy:
            result = buy_investment_to_portfolio(portfolio_name = portfolio_name ,db=db, transactionDetails = transactionDetails)
            return {f"Stock updated in portfolio: {result}"}
        elif transactionDetails.action == ActionType.sell:
            result = sell_investment_from_portfolio(portfolio_name = portfolio_name, db = db, transactionDetails = transactionDetails)
            return {f"stock sold in portfolio: {result}" }
        else:
            raise HTTPException(status_code=404, detail="Invalid Action")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        


# def get_portfolio_holdings():
# def add_a_stock_to_a_portfolio
# def remove a stock from a portfolio

