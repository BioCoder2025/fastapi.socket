import asyncio
import websockets
import random

async def send_emg():
    uri = "ws://localhost:8000/ws"
    while True:
        try:
            async with websockets.connect(
                uri,
                ping_interval=10,
                ping_timeout=10
            ) as ws:
                print("Connected to server")
                try:
                    while True:
                        value = random.gauss(0, 0.3)
                        value = max(min(value, 5), -5)
                        await ws.send(str(value))
                        print(f"Sent: {value}")
                        try:
                            response = await asyncio.wait_for(ws.recv(), timeout=1.0)
                            print(f"Received: {response}")
                        except asyncio.TimeoutError:
                            continue
                            
                        await asyncio.sleep(0.1)  # 데이터 전송 간격
                        
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"Connection closed: {e.code} - {e.reason}")
                    if e.code == 1011:
                        print("Internal server error occurred")
                    await asyncio.sleep(5)  # 재연결 전 대기
                    
        except Exception as e:
            print(f"Connection error: {str(e)}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(send_emg())
    except KeyboardInterrupt:
        print("Client stopped by user")