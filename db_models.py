from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float, DateTime, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase , relationship
from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy.orm import sessionmaker, Session

from datetime import datetime

import logging
from setup_logger import get_logger
logger = get_logger(__file__)
logging.getLogger('sqlalchemy.engine').handlers = logger.handlers
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


DATABASE_URL = 'sqlite:///./portfolio.db'
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

class DB_Portfolio(Base):
    __tablename__ = 'portfolios'

    portfolio_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] =  mapped_column(String, unique=True)

    investments: Mapped[List["Investments"]] = relationship("DB_Investment", back_populates="portfolio")

class DB_Investment(Base):
    __tablename__ = "investments"

    investment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    ticker_symbol: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    average_price_per_unit: Mapped[float] = mapped_column(Float)
    number_of_stocks_owned: Mapped[float] = mapped_column(Float)
    current_market_price: Mapped[float] = mapped_column(Float)
    market_price_refresh_timestamp : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolios.portfolio_id"))

    portfolio: Mapped["DB_Portfolio"] = relationship("DB_Portfolio", back_populates='investments')

    __table_args_ = (UniqueConstraint('portfolio_id', 'ticker_symbol', name='unique_portfolio_investment'))


# Create DDL 
Base.metadata.create_all(engine)


