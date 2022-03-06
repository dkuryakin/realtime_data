import asyncio
import json

from aiochclient import ChClient
from aiohttp import ClientSession
from fastapi import FastAPI, WebSocket

from common.typedef import PriceEvent
from common.utils import symbols
from .handler import PriceEventHandler
from .receiver import RealtimeDataReceiver
from .settings import Settings

settings = Settings()
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    app.state.price_event_handler = PriceEventHandler()
    app.state.symbols = symbols(
        settings.symbols_count,
        settings.symbols_prefix,
    )
    app.state.receiver = RealtimeDataReceiver(settings)
    app.state.subscription = asyncio.ensure_future(
        app.state.receiver.subscribe(app.state.price_event_handler.handle)
    )


@app.websocket("/price_events/{symbol}")
async def price_events(websocket: WebSocket, symbol: str):
    await websocket.accept()
    async with ClientSession() as sess:
        client = ChClient(sess, settings.clickhouse_dsn)
        price_event_list = await client.fetch("""
            SELECT *
            FROM market.prices_stats
            WHERE symbol = {symbol}
            ORDER BY timestamp DESC
            LIMIT 1000
        """, params={'symbol': symbol})
        msg = [
            json.loads(PriceEvent(**price_event).json())
            for price_event in reversed(price_event_list)
        ]
        await websocket.send_text(json.dumps(msg))
    while True:
        price_event: PriceEvent = await app.state.price_event_handler.get_price(symbol)
        if price_event is not None:
            await websocket.send_text(json.dumps([json.loads(price_event.json())]))
        await asyncio.sleep(settings.price_delay)


@app.get("/symbols")
async def list_symbols():
    return app.state.symbols
