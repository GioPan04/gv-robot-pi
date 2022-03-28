from GPIO.Motors import Motors
from GPIO.Ultrasonic import Ultrasonic
import RPi.GPIO as GPIO
from helpers import constrain,exit_handler
from distance_thread import DistanceThread

# Config
BASE_SPEED = 35
DISTANCE = 20
K = 0.3
MIN_SPEED = 25
MAX_SPEED = 50

# Pinout strategy:
# Sensor left: trig -> GPIO 4, echo -> GPIO 18
# Motors: in1 -> GPIO 12, in2 -> GPIO 13, ena -> GPIO 6, in3 -> GPIO 20, in4 -> GPIO 21, enb -> GPIO 26
# More about: https://www.waveshare.com/wiki/AlphaBot#Motor_driver_module

# Set BCM naming scheme
GPIO.setmode(GPIO.BCM)

# Initialize our sensors
car = Motors()
sensorL = Ultrasonic(4, 18)

distance_thread = DistanceThread("SensorL Thread", sensorL)
distance_thread.start()

# Run endlessly the motors, adjust the left and right speed by it's distance from the left wall
try:
  while True:
    distance = distance_thread.distance
    speed = K * (distance - DISTANCE)
    right = constrain(BASE_SPEED + speed, MIN_SPEED, MAX_SPEED)
    left = constrain(BASE_SPEED - speed, MIN_SPEED, MAX_SPEED)

    print(f"Left: {left} Right: {right} Distance: {distance}")
    car.setMotor(-left, right)
except KeyboardInterrupt:
  exit_handler(distance_thread)
except Exception as e:
  print(e)
  exit_handler(distance_thread)