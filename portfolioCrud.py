from db_models import SessionLocal
from db_models import DB_Investment, DB_Portfolio

from validatonModels import StockTransactionDetails

from sqlalchemy import select, insert

from setup_logger import get_logger
logger = get_logger(__name__)


def create_new_portfolio(name:str, db:SessionLocal):
        select_stmt = select(DB_Portfolio).filter_by(name=name)
        insert_stmt = insert(DB_Portfolio).values(name=name)
        existing_portfolio = db.execute(select_stmt).scalars().first() 
        if existing_portfolio:
            raise ValueError("Portfolio with the same name Already Exists")
        session.execute(insert_stmt)
        session.commit()
        return {"message":f"Protfolio '{name}' created successfully"}

def get_portfolio(name: str, db: SessionLocal):
    stmt = select(DB_Portfolio).filter_by(name=name)
    #with SessionLocal() as session:
    portfolios = db.execute(stmt)
    db_portfolio = portfolios.scalars().first()
    logger.debug(f"db_portfolio: {db_portfolio}")
    if not db_portfolio:
        raise ValueError("Portfolio Does not exists")
    return db_portfolio   #Return an object of Portfolio

def get_all_portfolios(limit: int, db: SessionLocal):
    stmt = select(DB_Portfolio).order_by(DB_Portfolio.portfolio_id).limit(limit=limit)
    logger.debug(f"stmt : {stmt}")
    portfolios = db.execute(stmt)
    db_portfolios = portfolios.scalars().all()
    logger.debug(f"returned: {db_portfolios}")
    logger.debug(f"{type(db_portfolios)}")
    return db_portfolios

def get_all_investments(portfolio_name: str, limit: int, db: SessionLocal):
    try:
        portfolio = get_portfolio(name=portfolio_name, db=db)
        investements = portfolio.investments[:limit]
        logger.debug(f"Fetching investments {investements} from portfolio {portfolio}")
        return investements
    except ValueError as e:
        logger.error(f"Error occured Fetching Portfolio, {e}")
        raise ValueError(f"Error occured Fetching Portfolio + {e}")
    


