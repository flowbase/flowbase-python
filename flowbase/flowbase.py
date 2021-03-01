"""
Copyright (c) 2021 Samuel Lampa <samuel.lampa@rilnet.com>
"""

import asyncio
import typing


def run(awaitable, **kwargs):
    asyncio.run(awaitable, **kwargs)


class Process:
    async def run(self):
        raise NotImplementedError(
            f"str(type(self)) can not be used directly, but must be subclassed"
        )


class Network(Process):
    _processes = {}

    def add_process(self, name: str, process: Process):
        self._processes[name] = process
        asyncio.create_task(process.run())

    async def run(self):
        [await p.run() for _, p in self._processes.items()]


class Port(asyncio.Queue):
    pass
