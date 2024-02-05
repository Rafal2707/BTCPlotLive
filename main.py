import json 
import websocket
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

assets = ['BTCUSDT']
assets = [coin.lower() + '@kline_1m' for coin in assets]
assets = '/'.join(assets)

x_vals = []
y_vals = []

fig, ax = plt.subplots()
plt.style.use('fivethirtyeight')

def manipulation(source):
    rel_data = source['data']['k']['c']
    event_time = pd.to_datetime(source['data']['E'], unit='ms')
    df = pd.DataFrame(rel_data, columns=[source['data']['s']], 
                      index=[event_time])
    df.index.name = 'timestamp'
    df = df.astype(float)
    df = df.reset_index()
    return df

def on_message(ws, message):
    message = json.loads(message)
    data = manipulation(message)
    x_vals.append(data['timestamp'])
    y_vals.append(data['BTCUSDT'])
    ax.clear()
    ax.plot(x_vals, y_vals)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

def ws_thread():
    socket = 'wss://stream.binance.com:9443/stream?streams=' + assets
    ws = websocket.WebSocketApp(socket, on_message=on_message)
    ws.run_forever()

ws_thread = threading.Thread(target=ws_thread)
ws_thread.start()

def animate(i):
    pass

ani = FuncAnimation(fig, animate, interval=1000)

plt.show()
