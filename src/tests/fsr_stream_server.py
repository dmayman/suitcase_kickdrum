import time
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Init Flask + WebSocket
app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

# ADC setup
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 8
fsr = AnalogIn(ads, ADS.P0)

@app.route("/")
def index():
    return render_template("index.html")

def stream_fsr():
    while True:
        v = fsr.voltage
        norm = max(0.0, min(1.0, v / 0.512))
        velocity = (1.0-norm) ** 4
        socketio.emit("fsr_data", {"voltage": v, "velocity": velocity})
        time.sleep(0.02)

@socketio.on("connect")
def handle_connect():
    print("Client connected")

if __name__ == "__main__":
    thread = threading.Thread(target=stream_fsr)
    thread.daemon = True
    thread.start()
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)