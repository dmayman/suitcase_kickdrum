import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set up I2C and ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 8

# Read from channel 0
fsr = AnalogIn(ads, ADS.P0)

print("Reading FSR...")
while True:
    raw_voltage = fsr.voltage
    normalized = max(0.0, min(1.0, raw_voltage / 0.512))  # Clamp to 0–1, gain=8 means ±0.512V range
    velocity = 1.0 - pow(normalized, 2.5)  # Exponential shaping
    print(f"Voltage: {raw_voltage:.3f} V | Velocity: {velocity:.3f}")
    time.sleep(0.01)