import asyncio
import logging

from aiokafka import AIOKafkaConsumer

from common.utils import symbols
from .settings import Settings
from .typedef import PriceEvent, PriceEventHandlerFunc


class RealtimeDataReceiver:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._symbols = symbols(
            settings.symbols_count,
            settings.symbols_prefix,
        )

        topics = [
            (settings.kafka_price_events_topic_prefix + symbol)
            for symbol in self._symbols
        ]
        self._consumer = AIOKafkaConsumer(*topics, bootstrap_servers=settings.kafka_dsn)

    async def subscribe(self, price_event_handler: PriceEventHandlerFunc):
        while True:
            try:
                await self._consumer.start()
                break
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logging.exception(e)
                await asyncio.sleep(1)

        try:
            async for msg in self._consumer:
                try:
                    price_event = PriceEvent.parse_raw(msg.value)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logging.exception(e)
                    continue
                await price_event_handler(price_event)
        finally:
            await self._consumer.stop()
