import flowbase


def main():
    net = flowbase.Network()

    # Initialize components
    hisayer = HiSayer()
    net.add_process("hisayer", hisayer)

    splitter = StringSplitter()
    net.add_process("hisayer", splitter)

    lowercaser = LowerCaser()
    net.add_process("hisayer", lowercaser)

    uppercaser = UpperCaser()
    net.add_process("hisayer", uppercaser)

    stringjoiner = StringJoiner()
    net.add_process("hisayer", stringjoiner)

    printer = Printer()
    net.add_process("hisayer", printer)

    # Connect network
    splitter.in_lines = hisayer.out_lines
    lowercaser.in_lines = splitter.out_leftpart
    uppercaser.in_lines = splitter.out_rightpart
    stringjoiner.in_leftpart = lowercaser.out_lines
    stringjoiner.in_rightpart = uppercaser.out_lines
    printer.in_lines = stringjoiner.out_lines

    # Run the full event loop
    net.run()


class HiSayer:
    out_lines = flowbase.Port()

    async def run(self):
        for i in range(20):
            await self.out_lines.put(f"Hi hi for the {i+1}:th time...")


class StringSplitter:
    in_lines = flowbase.Port()
    out_leftpart = flowbase.Port()
    out_rightpart = flowbase.Port()

    async def run(self):
        while not self.in_lines.empty():
            s = await self.in_lines.get()
            await self.out_leftpart.put(s[: int(len(s) / 2)])
            await self.out_rightpart.put(s[int(len(s) / 2) :])


class LowerCaser:
    in_lines = flowbase.Port()
    out_lines = flowbase.Port()

    async def run(self):
        while not self.in_lines.empty():
            s = await self.in_lines.get()
            await self.out_lines.put(s.lower())


class UpperCaser:
    in_lines = flowbase.Port()
    out_lines = flowbase.Port()

    async def run(self):
        while not self.in_lines.empty():
            s = await self.in_lines.get()
            await self.out_lines.put(s.upper())


class StringJoiner:
    in_leftpart = flowbase.Port()
    in_rightpart = flowbase.Port()
    out_lines = flowbase.Port()

    async def run(self):
        while not self.in_leftpart.empty() or not self.in_rightpart.empty():
            leftpart = await self.in_leftpart.get()
            rightpart = await self.in_rightpart.get()
            await self.out_lines.put(f"{leftpart}{rightpart}")


class Printer:
    in_lines = flowbase.Port()

    async def run(self):
        while not self.in_lines.empty():
            s = await self.in_lines.get()
            print(f"Printer got line: {s}")


if __name__ == "__main__":
    main()
