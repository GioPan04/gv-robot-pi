from GPIO.Motors import Motors
from GPIO.Ultrasonic import Ultrasonic
from threading import Thread
import RPi.GPIO as GPIO
from time import sleep
from helpers import constrain

# Config
BASE_SPEED = 20
DISTANCE = 20
K = 0.5
MIN_SPEED = 5
MAX_SPEED = 30

# Pinout strategy:
# Sensor left: trig -> GPIO 4, echo -> GPIO 18
# Motors: in1 -> GPIO 12, in2 -> GPIO 13, ena -> GPIO 6, in3 -> GPIO 20, in4 -> GPIO 21, enb -> GPIO 26
# More about: https://www.waveshare.com/wiki/AlphaBot#Motor_driver_module

# Set BCM naming scheme
GPIO.setmode(GPIO.BCM)

# Initialize our sensors
car = Motors()
sensorL = Ultrasonic(4, 18)

# Global variables, used by distance_calculator to calculate the distance between the sensors
run_thread = True
distance = 0

def distance_calculator():
  global distance
  GPIO.setmode(GPIO.BCM)

  # Run until the thread is stopped
  while run_thread:
    # Get the distances between the sensors, and use the sin/cos formula: rads = arcosin(distance / sensor_distance)
    distance = sensorL.measure()
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

# Run endlessly the motors, adjust the left and right speed by it's distance from the left wall
try:
  while True:
    right = constrain(BASE_SPEED - K * (distance - DISTANCE), MIN_SPEED, MAX_SPEED)
    left = constrain(BASE_SPEED + K * (distance - DISTANCE), MIN_SPEED, MAX_SPEED)
    
    print(f"Left: {left} Right: {right}")
    car.setMotor(-left, right)
except KeyboardInterrupt:
  exit_handler()
except Exception as e:
  print(e)
  exit_handler()