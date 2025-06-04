# FastAPI WebSocket EMG Visualization

이 프로젝트는 FastAPI 기반 WebSocket 서버와 실시간 EMG(근전도) 데이터 시각화 기능을 제공합니다.

## 주요 기능

- FastAPI를 이용한 WebSocket 서버 구현
- 클라이언트로부터 실시간 데이터 수신 및 에코 응답
- 수신된 데이터를 스레드 안전한 큐에 저장
- 별도의 스레드에서 실시간 데이터 시각화(EMG 데이터)

## 프로젝트 구조

```
main.py                # FastAPI 서버 및 시각화 실행
EMG/
  graph_visual.py      # 데이터 시각화 함수
  emg_test.py
  socket_procotol.py
```

## 설치 방법

1. Python 3.8 이상 설치
2. 필요한 패키지 설치:
   ```bash
   pip install fastapi uvicorn
   ```
   (추가적으로 `matplotlib` 등 시각화에 필요한 패키지가 있을 수 있습니다.)

## 실행 방법

```bash
python main.py
```

- 서버는 `127.0.0.1:8000`에서 WebSocket을 통해 통신합니다.
- 클라이언트는 `/ws` 엔드포인트로 접속하여 실시간 데이터를 전송할 수 있습니다.

## WebSocket 사용 예시

클라이언트에서 WebSocket 연결 후 float 값 전송:
```python
import websockets
import asyncio

async def send_data():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("1.23")
        response = await websocket.recv()
        print(response)

asyncio.run(send_data())
```

## 참고

- CORS가 허용되어 있어 외부 클라이언트에서도 접속 가능합니다.
- 데이터 시각화는 `EMG/graph_visual.py`의 `start_visualization` 함수에서 처리합니다.
