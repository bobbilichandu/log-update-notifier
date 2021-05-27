import asyncio

class FileListener:
    
    def __init__(self, path: str, polling_interval: float = 0.5) -> None:
        self.path = path
        self.pos = 0
        self.polling_interval = polling_interval
        self.update_position()

    async def listen(self):
        loop = asyncio.get_running_loop()
        while True:
            lines = await loop.run_in_executor(None, self.poll)
            for line in lines:
                if line.strip():
                    yield line
            await asyncio.sleep(self.polling_interval)

    def poll(self):
        with open(self.path, "r") as f:
            f.seek(self.pos)
            lines = f.readlines()
            self.pos = f.tell()
            return lines

    def update_position(self):
        with open(self.path, "r") as f:
            f.seek(self.pos)
            lines = f.readlines()
            self.pos = f.tell()