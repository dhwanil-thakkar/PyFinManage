from db_models import SessionLocal
from db_models import DB_Investment, DB_Portfolio

from sqlalchemy import select, insert

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='crud.log', encoding='utf-8', level=logging.DEBUG)


def create_new_portfolio(name:str):
        select_stmt = select(DB_Portfolio).filter_by(name=name)
        insert_stmt = insert(DB_Portfolio).values(name=name)
        with SessionLocal() as session:
            existing_portfolio = session.execute(select_stmt).scalars().first() 
            if existing_portfolio:
                raise ValueError("Portfolio with the same name Already Exists")
            session.execute(insert_stmt)
            session.commit()
            return {"message":f"Protfolio '{name}' created successfully"}

def get_portfolio(name: str):
    stmt = select(DB_Portfolio).filter_by(name=name)
    with SessionLocal() as session:
        portfolios = session.execute(stmt)
        db_portfolio = portfolios.scalars().first()
        logger.debug(f"db_portfolio: {db_portfolio}")
        if not db_portfolio:
            raise ValueError("Portfolio Does not exists")
        return db_portfolio   #Return an object of Portfolio

def get_all_portfolios(limit: int):
    stmt = select(DB_Portfolio).order_by(DB_Portfolio.portfolio_id).limit(limit=limit)
    logger.debug(f"stmt : {stmt}")
    with SessionLocal() as session:
        portfolios = session.execute(stmt)
        db_portfolios = portfolios.scalars().all()
        logger.debug(f"returned: {db_portfolios}")
        logger.debug(f"{type(db_portfolios)}")
        return db_portfolios
