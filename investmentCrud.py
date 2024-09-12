from db_models import SessionLocal
from db_models import DB_Investment, DB_Portfolio

from validatonModels import StockTransactionDetails, InvestmentDetails

from yfinance_utils import get_current_price, get_stock_name
from portfolioCrud import get_portfolio

from sqlalchemy import select, insert, update

from datetime import datetime

from setup_logger import get_logger
logger = get_logger(__name__)

def get_investment(portfolio: DB_Portfolio,investmentDetails: InvestmentDetails, db: SessionLocal) -> DB_Investment:

    investments = portfolio.investments
    logger.debug(f"investments in get_investment():  {investments}")
    for investment in investments:
        if (investment.ticker_symbol == investmentDetails.ticker_symbol):
            logger.debug(f"Investment Matched: {investment}")
            return investment

def create_new_investment(portfolio: DB_Portfolio, investmentDetails: InvestmentDetails, db: SessionLocal):
    
    logger.debug(f"Createing new Investment at create_new_invetment()")
    new_investment = DB_Investment(
        ticker_symbol = investmentDetails.ticker_symbol,
        average_price_per_unit = investmentDetails.average_price_per_unit,
        number_of_stocks_owned = investmentDetails.number_of_units,
        name = get_stock_name(ticker_symbol=investmentDetails.ticker_symbol),
        current_market_price = get_current_price(ticker_symbol=investmentDetails.ticker_symbol),
        market_price_refresh_timestamp = datetime.now(),
        portfolio_id = portfolio.portfolio_id
    )
    print(new_investment)
    logger.debug(f"new Investement: {new_investment}")
    try: 
        db.add(new_investment)
        db.commit()
        return new_investment
    except Exception as e:
        logger.error(f"Error Creating Investment: {e}")
        db.rollback()
        raise




def update_investment(portfolio: DB_Portfolio, investmentDetails: InvestmentDetails, db: SessionLocal):
    investment = get_investment(portfolio=portfolio, investmentDetails=investmentDetails, db=db)
    logger.debug(f"investment in update investment: {investment}")

    update_Stmt = (
        update(DB_Investment)
        .where(
            (DB_Investment.ticker_symbol == investmentDetails.ticker_symbol) &
            (investment.portfolio_id == portfolio.portfolio_id)
        )
        .values(
            average_price_per_unit=calc_avg_price(investmentDetails.average_price_per_unit), ##Calc fn()
            number_of_stocks_owned=calc_new_stock_inventory(investmentDetails.number_of_units), ##Add Func()
            current_market_price=get_current_price(ticker_symbol=investmentDetails.ticker_symbol),
            market_price_refresh_timestamp=datetime.now(),
        )
    )
    logger.debug(f"update Statement {update_Stmt}")

    try:
        db.execute(stmt)
        db_commit()
        return investment
    except Exception as e:
        logger.error(f"Error updating investment: {3}")
        db.rollback()
        raise



def calc_avg_price(investment: DB_Investment, investmentDetails: InvestmentDetails):
    
    investment.average_price_per_unit =  (
        ((investment.average_price_per_unit * investment.number_of_stocks_owned)
        + (investmentDetails.average_price_per_unit * investmentDetails.number_of_units))
        /(investment.number_of_stocks_owned + investmentDetails.number_of_units)
    )
    return investment

def calc_new_stock_inventory(foo):
    return foo




def buy_investment_to_portfolio(portfolio_name: str, transactionDetails: StockTransactionDetails, db: SessionLocal):
    try:
        portfolio = get_portfolio(name=portfolio_name, db=db)
        logger.debug(f"portfolio: {portfolio}")
        investment = get_investment(portfolio=portfolio, investmentDetails=transactionDetails, db=db)
        logger.debug(f"investment in buy_investment: {investment}")

        if investment:
            result  = update_investment(portfolio = portfolio, investmentDetails = transactionDetails, db=db)
            logger.debug(f"Update Investment resullt in buy investment: {result}")

        if not investment:
            logger.debug(f"No Investment Found, Creating new investment")
            result = create_new_investment(portfolio=portfolio, investmentDetails=transactionDetails, db=db)
            logger.debug(f"Create new Investement Result in buy investment: {result}")
                
        return (f"No exsisting investment found")

    except ValueError as e:
        logger.error(f"Error occured Fetching Portfolio, {e}")
        raise ValueError(f"Error occured Fetching Portfolio + {e}")
    
    


def sell_investment_from_portfolio (portfolio_name: str, transactionDetails: StockTransactionDetails, db: SessionLocal):
    return None
