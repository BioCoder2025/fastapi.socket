import queue  # 스레드 안전한 큐 사용
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def start_visualization(data_queue: queue.Queue):
    BUFFER_SIZE = 200
    data_buffer = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)

    fig, ax = plt.subplots()
    line, = ax.plot(list(data_buffer))
    ax.set_ylim(-8, 8)
    ax.set_title("Real-time EMG Visualization")
    ax.set_xlabel("Time")
    ax.set_ylabel("EMG Value")
    plt.tight_layout()

    def update(frame):
        while True:
            try:
                data_buffer.append(data_queue.get_nowait())
            except queue.Empty:
                break
        line.set_ydata(data_buffer)
        return line,

    ani = animation.FuncAnimation(
        fig, 
        update, 
        interval=50,  # 20 FPS (50ms)
        blit=True
    )
    plt.show()