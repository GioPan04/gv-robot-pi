import RPi.GPIO as GPIO
from time import sleep
from GPIO.Ultrasonic import Ultrasonic
from threading import Thread

class DistanceThread(Thread):
  def __init__(self, name: str, sensors: list[Ultrasonic]):
    super().__init__(name=name)
    self.distance = 0
    self.closest = 1
    self.__run_thread = True
    self.__sensors = sensors
  
  def run(self):
    """Read endlessly the value of the sensor"""
    GPIO.setmode(GPIO.BCM)

    # Run until the thread is stopped
    while self.__run_thread:
      distances = [None]*3
      for i,sensor in enumerate(self.__sensors):
        distances[i] = sensor.measure()
        sleep(.2)

      self.distance = min(distances)
      self.closest = distances.index(self.distance)

    print("Exiting from thread")
  
  def stop(self):
    self.__run_thread = False
    self.join()