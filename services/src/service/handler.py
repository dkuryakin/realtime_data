from .typedef import PriceEvent


class PriceEventHandler:
    def __init__(self):
        self._prices = {}

    async def handle(self, price_event: PriceEvent):
        self._prices[price_event.symbol] = price_event

    async def get_price(self, symbol: str) -> PriceEvent:
        return self._prices.get(symbol)
