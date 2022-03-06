import asyncio

from .generator import RealtimeDataGenerator
from .settings import Settings


async def main():
    settings = Settings()
    realtime_data_generator = RealtimeDataGenerator(settings)
    await realtime_data_generator.generate_price_events()


asyncio.run(main())
