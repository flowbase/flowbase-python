"""
Copyright (c) 2020 Samuel Lampa <samuel.lampa@rilnet.com>
"""

import asyncio
import typing


class Process:
    def run(self):
        raise NotImplementedError(
            f"str(type(self)) can not be used directly, but must be subclassed"
        )


class Network(Process):
    _processes = {}
    _driver_process = None

    def __init__(self):
        self._loop = asyncio.get_event_loop()

    def add_process(self, name: str, process: Process):
        self._processes[name] = process
        self._loop.create_task(process.run())
        self._driver_process = process

    def run(self):
        self._loop.run_until_complete(self._driver_process.run())


class Port(asyncio.Queue):
    pass
