# emg_test.py
import asyncio
import random
import numpy as np
import websockets

WS_URL = "ws://127.0.0.1:8000/ws"

def generate_emg_sample():
    noise = np.random.normal(0, 0.5)
    peak = random.uniform(3, 6) * random.choice([-1, 1]) if random.random() < 0.05 else 0
    return noise + peak

async def send_emg():
    async with websockets.connect(WS_URL) as ws:
        while True:
            value = generate_emg_sample()
            await ws.send(str(value))
            await asyncio.sleep(0.05)

if __name__ == "__main__":
    asyncio.run(send_emg())
