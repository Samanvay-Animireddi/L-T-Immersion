from machine import Pin, Timer
import time

# Define the input pin connected to the flow sensor signal
flow_pin = Pin(15, Pin.IN, Pin.PULL_UP)

# Pulse counter
pulse_count = 0

# Interrupt handler
def count_pulse(pin):
    global pulse_count
    pulse_count += 1

# Attach interrupt to the flow sensor pin
flow_pin.irq(trigger=Pin.IRQ_FALLING, handler=count_pulse)

# Flow rate calculation every second
def measure_flow(timer):
    global pulse_count
    pulses = pulse_count
    pulse_count = 0  # Reset counter

    # YFS402B: 7.5 pulses per liter/minute
    flow_rate = (pulses / 7.5)  # L/min

    print("Flow Rate: {:.2f} L/min".format(flow_rate))

# Start a timer to measure every 1 second
tim = Timer()
tim.init(mode=Timer.PERIODIC, period=1000, callback=measure_flow)

# Keep the program running
while True:
    time.sleep(1)
