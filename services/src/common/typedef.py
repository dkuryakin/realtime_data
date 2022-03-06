from typing import Callable, Awaitable
from pydantic import BaseModel, condecimal, conint
from decimal import Decimal


class PriceEvent(BaseModel):
    symbol: str
    timestamp: float
    price: condecimal(ge=Decimal(0))
    decimal_places: conint(gt=0)


PriceEventHandler = Callable[[PriceEvent], Awaitable[None]]