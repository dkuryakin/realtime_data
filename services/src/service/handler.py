from collections import defaultdict
from contextlib import asynccontextmanager
from uuid import uuid4

from common.utils import Channel
from .typedef import PriceEvent


class PriceEventHandler:
    def __init__(self):
        self._prices = {}
        self._channels = defaultdict(dict)

    async def handle(self, price_event: PriceEvent):
        symbol = price_event.symbol
        if symbol not in self._channels:
            return
        for receiver in self._channels[symbol].values():
            await receiver.send(price_event)

    @asynccontextmanager
    async def subscribe(self, symbol: str):
        key = uuid4()
        channel = Channel()
        self._channels[symbol][key] = channel
        try:
            yield channel
        finally:
            self._channels[symbol].pop(key)
