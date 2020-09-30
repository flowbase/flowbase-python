import asyncio


def main():
    loop = asyncio.get_event_loop()

    # Initialize components
    hisayer = HiSayer()
    loop.create_task(hisayer.run())

    splitter = StringSplitter()
    loop.create_task(splitter.run())

    lowercaser = LowerCaser()
    loop.create_task(lowercaser.run())

    uppercaser = UpperCaser()
    loop.create_task(uppercaser.run())

    stringjoiner = StringJoiner()
    loop.create_task(stringjoiner.run())

    printer = Printer()
    loop.create_task(printer.run())

    # Connect network
    splitter.in_lines = hisayer.out_lines
    lowercaser.in_lines = splitter.out_leftpart
    uppercaser.in_lines = splitter.out_rightpart
    stringjoiner.in_leftpart = lowercaser.out_lines
    stringjoiner.in_rightpart = uppercaser.out_lines
    printer.in_lines = stringjoiner.out_lines

    # Run the full event loop
    loop.run_until_complete(printer.run())


class HiSayer:
    out_lines = asyncio.Queue()

    async def run(self):
        for i in range(20):
            self.out_lines.put_nowait(f"Hi hi for the {i+1}:th time...")
            self.out_lines.task_done()


class StringSplitter:
    in_lines = asyncio.Queue()
    out_leftpart = asyncio.Queue()
    out_rightpart = asyncio.Queue()

    async def run(self):
        while not self.in_lines.empty():
            s = await self.in_lines.get()
            self.out_leftpart.put_nowait(s[: int(len(s) / 2)])
            self.out_rightpart.put_nowait(s[int(len(s) / 2) :])


class LowerCaser:
    in_lines = asyncio.Queue()
    out_lines = asyncio.Queue()

    async def run(self):
        while not self.in_lines.empty():
            s = await self.in_lines.get()
            self.out_lines.put_nowait(s.lower())


class UpperCaser:
    in_lines = asyncio.Queue()
    out_lines = asyncio.Queue()

    async def run(self):
        while not self.in_lines.empty():
            s = await self.in_lines.get()
            self.out_lines.put_nowait(s.upper())


class StringJoiner:
    in_leftpart = asyncio.Queue()
    in_rightpart = asyncio.Queue()
    out_lines = asyncio.Queue()

    async def run(self):
        while not self.in_leftpart.empty() or not self.in_rightpart.empty():
            leftpart = await self.in_leftpart.get()
            rightpart = await self.in_rightpart.get()
            self.out_lines.put_nowait(f"{leftpart}{rightpart}")


class Printer:
    in_lines = asyncio.Queue()

    async def run(self):
        while not self.in_lines.empty():
            s = await self.in_lines.get()
            print(f"Printer got line: {s}")


if __name__ == "__main__":
    main()
