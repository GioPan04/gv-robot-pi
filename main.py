from GPIO.Motors import Motors
from GPIO.Ultrasonic import Ultrasonic
import RPi.GPIO as GPIO
from helpers import exit_handler,calculate_speed
from distance_thread import DistanceThread

# Pinout strategy:
# Sensor left: trig -> GPIO 4, echo -> GPIO 18
# Motors: in1 -> GPIO 12, in2 -> GPIO 13, ena -> GPIO 6, in3 -> GPIO 20, in4 -> GPIO 21, enb -> GPIO 26
# More about: https://www.waveshare.com/wiki/AlphaBot#Motor_driver_module

# Set BCM naming scheme
GPIO.setmode(GPIO.BCM)

# Initialize our sensors
car = Motors()
sensorT = Ultrasonic(4, 18)
sensorM = Ultrasonic(4, 18)
sensorB = Ultrasonic(4, 18)
distance_thread = DistanceThread("SensorL Thread", [sensorT, sensorM, sensorB])


if __name__ == '__main__':
  distance_thread.start()

  # Run endlessly the motors, adjust the left and right speed by it's distance from the left wall
  try:
    while True:
      distance = distance_thread.distance
      (left, right) = calculate_speed(distance)

      print(f"Left: {left} Right: {right} Distance: {distance}")
      car.setMotor(-left, right)
  except KeyboardInterrupt:
    exit_handler(distance_thread)
  except Exception as e:
    print(e)
    exit_handler(distance_thread)
