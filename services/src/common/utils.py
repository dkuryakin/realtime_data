from asyncio import Queue


def symbols(symbols_count: int, symbols_prefix: str):
    digits = len(str(symbols_count - 1))
    fmt = f"%0{digits}d"
    return [
        (symbols_prefix + fmt % i)
        for i in range(symbols_count)
    ]


class Channel:
    def __init__(self):
        self._queue = Queue()

    async def send(self, item):
        return await self._queue.put(item)

    async def recv(self):
        return await self._queue.get()
