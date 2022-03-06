from typing import Callable, Awaitable
from common.typedef import PriceEvent


PriceEventHandlerFunc = Callable[[PriceEvent], Awaitable[None]]