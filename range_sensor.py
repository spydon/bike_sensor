import RPi.GPIO as GPIO
import time
import signal
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TRIG = 2              # The pin that gets triggered from the echo
DIST_TRIGGER = 60     # The length in centimeters that the led should light up
ECHO_PIN = [9,10,11]  # The echo pins of the ultra sonic sensors
LED_PIN = [7,8,25]    # The pins of the leds

# Used to read distance from ECHO pin
# It uses the amount of time from sending
# out a signal until it is received again
# and then converts it to centimeters
def read_distance(ECHO):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    
    pulse_end = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

# Sets up all the pins to be input or output
# pins and whether they should be on or not 
def pin_setup():
    GPIO.setup(TRIG,GPIO.OUT)
    for pin in ECHO_PIN:
        GPIO.setup(pin,GPIO.IN)
    
    for pin in LED_PIN:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)

    GPIO.output(TRIG, False)
    print "Waiting For Sensors To Settle"
    time.sleep(2)

# Checks the distance to the nearest object from
# the sensor argument and lights up a led if there
# is an object closer than DIST_TRIGGER
def run_sensor(sensor):
    dist = read_distance(ECHO_PIN[sensor])
    print "Distance ",sensor,":",dist,"cm"
    if dist < DIST_TRIGGER:
        GPIO.output(LED_PIN[sensor], False)
    else:
        GPIO.output(LED_PIN[sensor], True)
    time.sleep(0.05)

# Cleaning up and exiting the program
def signal_handler(signal, frame):
    GPIO.cleanup()
    print "\nCleaned up, now quiting"
    sys.exit(0)

# Makes sure that the program sets up the pins and
# keeps checking the sensors
def main():
    signal.signal(signal.SIGINT, signal_handler)
    print "Starting Checking For Bikes"
    pin_setup()
    while True:
        for X in range(len(ECHO_PIN)):
            run_sensor(X)

main()
