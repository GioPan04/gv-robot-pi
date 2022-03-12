from AlphaBot import AlphaBot
from Ultrasonic import Ultrasonic
from threading import Thread
import RPi.GPIO as GPIO
from time import sleep
from math import asin

BASE_SPEED = 25
RADS_MULTIPLIER = 5
SENSORS_DISTANCE = 11

# Set BCM naming scheme
GPIO.setmode(GPIO.BCM)

# Initialize our sensors
car = AlphaBot()
sensorT = Ultrasonic(4, 18)
sensorB = Ultrasonic(17, 27)

# Global variables, used by distance_calculator to calculate the distance between the sensors
rads = 0
run_thread = True

def distance_calculator():
  global rads

  # Run until the thread is stopped
  while run_thread:
    # Get the distances between the sensors, and use the sin/cos formula: rads = arcosin(distance / sensor_distance)
    distanceT = sensorT.measure()
    distanceB = sensorB.measure()
    c = distanceT - distanceB
    if abs(c) <= SENSORS_DISTANCE:
      s = c / SENSORS_DISTANCE
      rads = asin(s)
    sleep(.5)
  print("Exiting from thread")


distance_thread = Thread(target=distance_calculator)
distance_thread.start()

# When the program exit cleanup the GPIO and stop the thread
def exit_handler():
  global run_thread
  run_thread = False
  print("Exiting...")
  GPIO.cleanup()
  distance_thread.join()

# Run endlessly the motors, adjust the left speed by it's distance
try:
  while True:
    left = BASE_SPEED + (rads * RADS_MULTIPLIER)
    print(f"Left: {left}")
    car.setMotor(left, -BASE_SPEED)      
except:
  exit_handler()