from pydantic import BaseModel
from enum import Enum



class ActionType(Enum):
    buy = 'buy'
    sell = 'sell'

# class StockTransactionDetails(BaseModel):
#     ticker_symbol: str
#     quantity: float
#     price: float
#     action: ActionType

class InvestmentDetails(BaseModel):
    ticker_symbol: str
    average_price_per_unit: float
    number_of_units: float

class InvestmentTransactionDetails(InvestmentDetails):
    action: ActionType