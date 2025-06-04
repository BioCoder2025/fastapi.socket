import threading
import queue  # 스레드 안전한 큐 사용
from fastapi import FastAPI, WebSocket
import uvicorn
from EMG.graph_visual import start_visualization
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()
data_queue = queue.Queue(maxsize=100)  # 스레드 안전한 큐

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            # print(f"Received: {data}")
            await websocket.send_text(f"Echo: {data}")
            try:
                value = float(data)
            except ValueError:
                print(f"Invalid float value: {data}")
                continue
                
            try:
                data_queue.put_nowait(value)
            except queue.Full:
                print("Queue full - discarding data")
                
        except Exception as e:
            print(f"WebSocket error: {e}")
            break

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    # FastAPI 서버를 별도의 스레드에서 실행
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # 메인 스레드에서 시각화 실행
    start_visualization(data_queue=data_queue)