import asyncio
import random
import time
from decimal import Decimal

from aiokafka import AIOKafkaProducer

from common.typedef import PriceEvent
from common.utils import symbols
from .settings import Settings


class RealtimeDataGenerator:
    """This class generates random price change events & send this data to queue."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._symbols = symbols(
            self._settings.symbols_count,
            self._settings.symbols_prefix,
        )
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_dsn
        )

    @staticmethod
    async def _prices(price: float):
        while True:
            yield price
            price += random.random() - 0.5
            if price < 0:
                price = 0
            await asyncio.sleep(random.random() * 2)

    async def _generate_symbol_price_events(self, symbol: str):
        decimal_places = random.randint(1, 6)
        initial_price = 0  # 10 + random.random() * 100
        precision = Decimal('.' + '0' * decimal_places)
        topic = self._settings.kafka_price_events_topic_prefix + symbol

        async for price in self._prices(initial_price):
            price_event = PriceEvent(
                symbol=symbol,
                timestamp=time.time(),
                price=Decimal(price).quantize(precision),
                decimal_places=decimal_places,
            )
            msg = price_event.json().encode()
            await self._producer.send_and_wait(topic, msg)
            await self._producer.send_and_wait(self._settings.kafka_ch_topic, msg)

    async def generate_price_events(self):
        await self._producer.start()
        try:
            jobs = [
                self._generate_symbol_price_events(symbol)
                for symbol in self._symbols
            ]
            await asyncio.gather(*jobs)
        finally:
            await self._producer.stop()
