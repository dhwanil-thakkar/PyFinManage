from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from datetime import datetime

DATABASE_URL = 'sqlite:///./portfolio.db'
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

class DB_Portfolio(Base):
    __tablename__ = 'portfolios'

    portfolio_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] =  mapped_column(unique=True)
    investments: Mapped[List["DB_Investment"]] = relationship("DB_Investment", back_populates="portfolio")

class DB_Investment(Base):
    __tablename__ = "investments"

    investment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker_symbol: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    average_price_per_unit: Mapped[float] = mapped_column()
    number_of_stocks_owned: Mapped[float] = mapped_column()
    current_market_price: Mapped[float] = mapped_column()
    market_price_refresh_timestamp : Mapped[datetime] = mapped_column()
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.portfolio_id"))

    portfolio: Mapped["DB_Portfolio"] = relationship("DB_Portfolio", back_populates='investments')


# Create DDL 
Base.metadata.create_all(engine)


## how to use these db_models

# with SessionLocal() as session:

#     portfolio_1 = Portfolio()

#     Apple_investment = Investment(
#         ticker_symbol = "APPL",
#         name = "Apple",
#         average_price_per_unit = 150.0,
#         number_of_stocks_owned = 10,
#         current_market_price = 155.43,
#         market_price_refresh_timestamp = datetime.now(),
#         portfolio = portfolio_1
#     )

#     session.add(portfolio_1)
#     session.add(Apple_investment)
#     session.commit()

#     #Query

#     portfolio = session.query(Portfolio).first()
#     investments = session.query(Investment).all()

#     print(f"Portfolio ID: {portfolio.portfolio_id}")
#     for investment in investments:
#          print(f"Investment Ticker: {investment.ticker_symbol}, Name: {investment.name}")