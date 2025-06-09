from umqtt.simple import MQTTClient
import time
import network
from machine import Pin, Timer
import urequests
import ubinascii

# ========== Wi-Fi credentials ==========
ssid = "chitti controller"
password = "19eee212"

# ========== Twilio Credentials ==========
TWILIO_ACCOUNT_SID = "ACa2b8e72f4757c8c157715e64c12ad22a"
TWILIO_AUTH_TOKEN = "2441b319ad3b88cfa097eb36656671d8"
TWILIO_FROM_NUMBER = "+12182479992"
USER_PHONE_NUMBER = "+918348802666"  # 🔁 Replace with your real number

# ========== ThingSpeak MQTT credentials ==========
MQTT_BROKER = "mqtt3.thingspeak.com"
PORT = 1883
CLIENT_ID = "LyE2MR4UDiAuNy4TDDoXLAk"
USERNAME = "LyE2MR4UDiAuNy4TDDoXLAk"
PASSWORD = "MPImL/Fh9NTFSywZpdc70krh"
CHANNEL_ID = "2984369"
TOPIC = f"channels/{CHANNEL_ID}/publish/fields/field1"

# ========== Flow Sensor Setup ==========
flow_pin = Pin(15, Pin.IN, Pin.PULL_UP)
pulse_count = 0

def count_pulse(pin):
    global pulse_count
    pulse_count += 1

flow_pin.irq(trigger=Pin.IRQ_FALLING, handler=count_pulse)

# ========== Wi-Fi Connection ==========
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    time.sleep(1)
print("✅ Wi-Fi connected")

# ========== MQTT Publishing ==========
def send_mqtt(flow_rate):
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=PORT, user=USERNAME, password=PASSWORD)
        client.connect()
        print("✅ MQTT connected")

        payload = "{:.2f}".format(flow_rate)  # Just the number
        client.publish(TOPIC.encode(), payload.encode())
        print("📤 Sent flow rate: {:.2f} L/min".format(flow_rate))

        client.disconnect()
    except Exception as e:
        print("❌ MQTT Failed:", e)

# ========== Twilio SMS ==========
def send_sms(message):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = f"To={USER_PHONE_NUMBER}&From={TWILIO_FROM_NUMBER}&Body={message}"
    auth = ubinascii.b2a_base64(f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}".encode()).decode().strip()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = urequests.post(url, data=data, headers=headers)
        if response.status_code in [200, 201]:
            print("✅ SMS sent successfully")
        else:
            print(f"❌ SMS failed: {response.status_code} {response.text}")
        response.close()
    except Exception as e:
        print("❌ Exception sending SMS:", e)

# ========== Flow Measurement ==========
def measure_flow(timer):
    global pulse_count
    pulses = pulse_count
    pulse_count = 0
    flow_rate = pulses / 7.5  # YFS402B: 7.5 pulses per L/min
    print("💧 Flow Rate: {:.2f} L/min".format(flow_rate))

    if flow_rate < 0.3 or flow_rate > 50
    .0:
        alert_msg = f"⚠️ Alert! \n  Flow rate out of range: {flow_rate:.2f} L/min"
        print(alert_msg)
        send_sms(alert_msg)
    else:
        send_mqtt(flow_rate)

# ========== Start Periodic Timer ==========
tim = Timer()
tim.init(mode=Timer.PERIODIC, period=10000, callback=measure_flow)  # Every 10 sec

# ========== Main Loop ==========
while True:
    time.sleep(1)
 