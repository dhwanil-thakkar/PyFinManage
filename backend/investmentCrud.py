from db_models import SessionLocal
from db_models import DB_Investment, DB_Portfolio

from validatonModels import InvestmentTransactionDetails, ActionType

from yfinance_utils import get_current_price, get_stock_name
from portfolioCrud import get_portfolio

from sqlalchemy import select, insert, update, delete

from datetime import datetime

from setup_logger import get_logger
logger = get_logger(__name__)

def get_investment_from_portfolio(portfolio: DB_Portfolio, investmentTransactionDetails: InvestmentTransactionDetails, db: SessionLocal) -> DB_Investment:

    investments = portfolio.investments
    logger.debug(f"investments in get_investment():  {investments}")
    logger.debug(f"investmentTransactionDetails: {investmentTransactionDetails.ticker_symbol}")
    for investment in investments:
        logger.debug(f"invesmment in portfolios  {investment.ticker_symbol}")
        if (investment.ticker_symbol == investmentTransactionDetails.ticker_symbol):
            logger.debug(f"Investment Matched: {investment}")
            return investment

def create_new_investment(portfolio: DB_Portfolio, investmentTransactionDetails: InvestmentTransactionDetails, db: SessionLocal):
    
    logger.debug(f"Createing new Investment at create_new_invetment()")
    new_investment = DB_Investment(
        ticker_symbol = investmentTransactionDetails.ticker_symbol,
        average_price_per_unit = investmentTransactionDetails.average_price_per_unit,
        number_of_stocks_owned = investmentTransactionDetails.number_of_units,
        name = get_stock_name(ticker_symbol=investmentTransactionDetails.ticker_symbol),
        current_market_price = get_current_price(ticker_symbol=investmentTransactionDetails.ticker_symbol),
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




def update_investment(portfolio: DB_Portfolio, investment: DB_Investment, investmentTransactionDetails: InvestmentTransactionDetails, db: SessionLocal):
#    investment = get_investment(portfolio=portfolio, investmentTransactionDetails=investmentTransactionDetails, db=db)
    logger.debug(f"investment in update investment: {investment}")

    update_stmt = (
        update(DB_Investment)
        .where(
            (DB_Investment.ticker_symbol == investmentTransactionDetails.ticker_symbol) &
            (investment.portfolio_id == portfolio.portfolio_id)
        )
        .values(
            average_price_per_unit=calc_avg_price(investment=investment, investmentTransactionDetails=investmentTransactionDetails), ##Calc fn()
            number_of_stocks_owned=calc_new_stock_inventory(investment=investment, investmentTransactionDetails=investmentTransactionDetails), ##Add Func()
            current_market_price=get_current_price(ticker_symbol=investmentTransactionDetails.ticker_symbol),
            market_price_refresh_timestamp=datetime.now(),
        )
    )
    logger.debug(f"update Statement {update_stmt}")

    try:
        db.execute(update_stmt)
        db.commit()
        return investment
    except Exception as e:
        logger.error(f"Error updating investment: {3}")
        db.rollback()
        raise

def remove_investment_from_portfolio(investment: DB_Investment, db: SessionLocal):
    try:
        delete_stmt= delete(DB_Investment).where(DB_Investment.investment_id == investment.investment_id)
        result = db.execute(delete_stmt)
        db.commit()
        logger.debug(f"remove_result: {result}")
        return None
    except Exception as e:
        raise RuntimeError ("Error Occured removing investment from the database, Try again later.")


def calc_avg_price(investment: DB_Investment, investmentTransactionDetails: InvestmentTransactionDetails):

    if(investmentTransactionDetails.action == ActionType.buy):    

        investment.average_price_per_unit =  (
            ((investment.average_price_per_unit * investment.number_of_stocks_owned)
            + (investmentTransactionDetails.average_price_per_unit * investmentTransactionDetails.number_of_units))
            /(investment.number_of_stocks_owned + investmentTransactionDetails.number_of_units)
        )

    if(investmentTransactionDetails == ActionType.sell):

        investment.average_price_per_unit =  (
            ((investment.average_price_per_unit * investment.number_of_stocks_owned)
            - (investmentTransactionDetails.average_price_per_unit * investmentTransactionDetails.number_of_units))
            /(investment.number_of_stocks_owned - investmentTransactionDetails.number_of_units)
        )

    return investment.average_price_per_unit

def calc_new_stock_inventory(investment: DB_Investment, investmentTransactionDetails: InvestmentTransactionDetails):

    if(investmentTransactionDetails.action == ActionType.buy):

        investment.number_of_stocks_owned = (investment.number_of_stocks_owned + investmentTransactionDetails.number_of_units)

    elif(investmentTransactionDetails.action == ActionType.sell):

        investment.number_of_stocks_owned = (investment.number_of_stocks_owned - investmentTransactionDetails.number_of_units)


    return investment.number_of_stocks_owned




def buy_investment_to_portfolio(portfolio: DB_Portfolio, investmentTransactionDetails: InvestmentTransactionDetails, db: SessionLocal):
    try:
        logger.debug(f"portfolio: {portfolio}")
        investment = get_investment_from_portfolio(portfolio=portfolio, investmentTransactionDetails = investmentTransactionDetails, db = db)
        logger.debug(f"investment in buy_investment: {investment}")

        if (investmentTransactionDetails.average_price_per_unit <=0):
            raise ValueError("Average price per unit of the needs to be greater than 0")

        if (investmentTransactionDetails.number_of_units <=0):
            raise ValueError("Number of units for the transaction should be greater than 0")

        if not investment:
            logger.debug(f"No Investment Found, Creating new investment")
            result = create_new_investment(portfolio=portfolio, investmentTransactionDetails=investmentTransactionDetails, db=db)
            logger.debug(f"Create new Investement Result in buy investment: {result}")
            return result

        if investment:
            result  = update_investment(portfolio=portfolio, investment=investment, investmentTransactionDetails=investmentTransactionDetails, db=db)
            logger.debug(f"Update Investment resullt in buy investment: {result}")
            return result
                
        return (f"No exsisting investment found")

    except ValueError as e:
        logger.error(f"Error occured Fetching Portfolio, {e}")
        raise ValueError(f"Error occured Fetching Portfolio + {e}")
    
    



def sell_investment_from_portfolio (portfolio: DB_Portfolio, investmentTransactionDetails: InvestmentTransactionDetails, db: SessionLocal):
    try:
        investment = get_investment_from_portfolio(portfolio=portfolio, investmentTransactionDetails=investmentTransactionDetails, db=db)
        logger.debug(f"Investment in sell_investment: {investment}")


        if not investment:
            raise ValueError("No Investment Found")

        if (investmentTransactionDetails.average_price_per_unit <=0):
            raise ValueError("Average price per unit of the needs to be greater than 0")

        if (investmentTransactionDetails.number_of_units <=0):
            raise ValueError("Number of units for the transaction should be greater than 0")
        
        if (investmentTransactionDetails.number_of_units > investment.number_of_stocks_owned):
            raise ValueError(f"Cannot sell more than you own in the portfolio, current quantity: {investment.number_of_stocks_owned}")

        if (investmentTransactionDetails.number_of_units == investment.number_of_stocks_owned):
            result = remove_investment_from_portfolio(investment=investment, db=db)
            return result

        if investment:
            result = update_investment(portfolio=portfolio, investment=investment, investmentTransactionDetails=investmentTransactionDetails, db=db)
            logger.debug(f"Updated investment result in sell_investment: {result}")
            return result

    except ValueError as e:
        logger.error(f"Error occured Fetching Portfolio, {e}")
        raise ValueError(f"Error occured Fetching Portfolio, {e}")


# def sell_investment_from_portfolio (portfolio_name: str, transactionDetails: InvestmentTransactionDetails, db: SessionLocal):
#     try:
#         portfolio = get_portfolio(name=portfolio_name, db=db)
#         investment = get_investment(portfolio=portfolio, investmentTransactionDetails = transactionDetails, db=db)

#         if not investment:
#             logger.error(f"No Investment Exsists cannot delete")

#         if investment:
#             try:
#                 result = update_investment(portfolio=portfolio, investmentTransactionDetails= transactionDetails, db=db)
#                 return result
#             except Exception as e:
#                 return (f"Error occured in updating investment: {e}")


#     except Exception as e:
#         return (f"Error Occured selling investment: {e}")