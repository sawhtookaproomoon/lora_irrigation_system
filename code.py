import board
import busio
import displayio
import terminalio
import adafruit_dht
from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306
import time

# Release any resources currently in use for the displays
displayio.release_displays()

# Define the I2C interface using explicit pins for the Pico
i2c = busio.I2C(board.GP1, board.GP0)

# Define the display bus
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# Define the display
WIDTH = 128
HEIGHT = 32
BORDER = 2

display = SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Create a display group
splash = displayio.Group()

# Draw initial label
text = "Initializing..."
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=12, y=12)
splash.append(text_area)

# Set the display root group
display.root_group = splash

# Initialize the DHT11 sensor
dht_device = adafruit_dht.DHT11(board.GP15)

while True:
    try:
        # Read temperature and humidity from the DHT11 sensor
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        # Update the text on the OLED display
        text_area.text = f"Temp: {temperature} C\nHumidity: {humidity} %"
        
    except RuntimeError as error:
        # Handle errors
        text_area.text = "Error\nReading sensor"
        print(error.args[0])
    
    time.sleep(2)
