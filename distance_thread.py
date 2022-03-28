import RPi.GPIO as GPIO
from time import sleep
from GPIO.Ultrasonic import Ultrasonic
from threading import Thread
from random import randint

class DistanceThread(Thread):
  def __init__(self, name: str, sensor: Ultrasonic):
    super().__init__(name=name)
    self.distance = 0
    self.__run_thread = True
    self.__sensor = sensor
  
  def run(self):
    """Read endlessly the value of the sensor"""
    GPIO.setmode(GPIO.BCM)

    # Run until the thread is stopped
    while self.__run_thread:
      self.distance = self.__sensor.measure()
      sleep(.3)
    print("Exiting from thread")
  
  def stop(self):
    self.__run_thread = False
    self.join()