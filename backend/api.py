from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from db_models import SessionLocal, DB_Investment, DB_Portfolio
#from portfolioManager import Portfolio, Stock

from validatonModels import InvestmentTransactionDetails, ActionType
from portfolioCrud import get_all_portfolios, create_new_portfolio, get_all_investments, get_portfolio
from investmentCrud import buy_investment_to_portfolio, sell_investment_from_portfolio


from setup_logger import get_logger

logger = get_logger(__file__)



app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        portfolio = get_portfolio(name=name, db=db)
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
def add_or_remove_stock_to_portfolio(portfolio_name:str, investmentTransactionDetails: InvestmentTransactionDetails, db: SessionLocal = Depends(get_db)):
    try:
        portfolio = get_portfolio(name=portfolio_name, db=db)

#       logger.debug(transactionDetails)
        if investmentTransactionDetails.action == ActionType.buy:
            result = buy_investment_to_portfolio(portfolio=portfolio, db=db, investmentTransactionDetails=investmentTransactionDetails)
            return {
                f"portfolio : {portfolio.to_dict()}",
                f"Investments: {result.to_dict()}",
            }
        elif investmentTransactionDetails.action == ActionType.sell:
            result = sell_investment_from_portfolio(portfolio=portfolio, db=db, investmentTransactionDetails=investmentTransactionDetails)

            if result is None:
                return {
                    f"portfolio: {portfolio.to_dict()}",
                    f"Investments: None"
                }

            return {
                f"portfolio : {portfolio.to_dict()}",
                f"Investments: {result.to_dict()}",
            }
        else:
            raise HTTPException(status_code=404, detail="Invalid Action")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error Processing Trasaction: " + str(e))
        


# def get_portfolio_holdings():
# def add_a_stock_to_a_portfolio
# def remove a stock from a portfolio

