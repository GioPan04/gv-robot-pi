import RPi.GPIO as GPIO # type: ignore
from time import sleep
from GPIO.Ultrasonic import Ultrasonic
from core.base_thread import BaseThread

class DistanceThread(BaseThread):
  def __init__(self, name: str, sensors: list[Ultrasonic]):
    super().__init__(name=name)
    self.distance = 0
    self.closest = 1
    self.__sensors = sensors
  
  def setup(self):
    GPIO.setmode(GPIO.BCM)
  
  def tick(self):
    """Read endlessly the value of the sensor"""
    distances = [None]*3
    for i,sensor in enumerate(self.__sensors):
      distances[i] = sensor.measure()
      self.print(f"{i}: {self.distance}")
      sleep(.2)

    self.distance = min(distances)
    self.closest = distances.index(self.distance)
    self.print(f"Distance: {self.distance} by {self.closest}")