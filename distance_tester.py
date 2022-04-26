from time import sleep
from GPIO.Ultrasonic import Ultrasonic
import RPi.GPIO as GPIO

"""
  This file is only for testing the left sensor
"""

GPIO.setmode(GPIO.BCM)

sensor = Ultrasonic(4, 18)

while True:
  distance = sensor.measure()
  print(f"{distance}cm")
  sleep(0.3)