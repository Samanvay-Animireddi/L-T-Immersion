import network
import urequests
from machine import Pin, Timer
import time

# WiFi credentials
SSID = "chitti controller"         # Replace with your WiFi SSID
PASSWORD = "19eee212"                # Replace with your WiFi password

# ThingSpeak settings
THINGSPEAK_API_KEY = "R532GHPMRR66KOYD"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

# Setup for onboard LED (GPIO 25)
led = Pin("LED", Pin.OUT)
led.off()

# Flow sensor setup (YFS402B connected to GPIO 15)
flow_pin = Pin(15, Pin.IN, Pin.PULL_UP)
pulse_count = 0

# Interrupt for pulse counting
def count_pulse(pin):
    global pulse_count
    pulse_count += 1

flow_pin.irq(trigger=Pin.IRQ_FALLING, handler=count_pulse)

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to WiFi", end='')
    while not wlan.isconnected():
        print(".", end='')
        time.sleep(1)
    print("\n✅ Connected:", wlan.ifconfig())

connect_wifi()

# Send data to ThingSpeak every 5 seconds
def send_data(timer):
    global pulse_count
    pulses = pulse_count
    pulse_count = 0

    # YFS402B: 7.5 pulses per liter/min
    flow_rate = pulses / 7.5

    print("Flow Rate: {:.2f} L/min".format(flow_rate))

    try:
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={flow_rate:.2f}"
        response = urequests.get(url)

        if response.status_code == 200:
            print("✅ Data sent successfully")
            led.on()
            time.sleep(0.2)
            led.off()
        else:
            print("❌ Failed to send data: Status", response.status_code)

        response.close()

    except Exception as e:
        print("❌ Failed to send data:", e)

# Start the periodic timer (every 5 seconds)
timer = Timer()
timer.init(mode=Timer.PERIODIC, period=1000, callback=send_data)

# Keep the main program running
while True:
    time.sleep(1)
