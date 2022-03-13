from decimal import Decimal
from typing import Awaitable, Callable, List

from pydantic import BaseModel, condecimal, conint


class PriceEvent(BaseModel):
    symbol: str
    timestamp: float
    price: condecimal(ge=Decimal(0))
    decimal_places: conint(gt=0)


class PriceEventList(BaseModel):
    __root__: List[PriceEvent]


PriceEventHandler = Callable[[PriceEvent], Awaitable[None]]
