import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set up I2C and ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Read from channel 0
fsr = AnalogIn(ads, ADS.P0)

print("Reading FSR...")
while True:
    print(f"Voltage: {fsr.voltage:.3f} V")
    time.sleep(0.05)

    