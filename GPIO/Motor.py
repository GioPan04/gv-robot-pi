import RPi.GPIO as GPIO # type: ignore
from core.base_thread import BaseThread
from time import sleep


class Motor(BaseThread):
  
  def __init__(self, name: str, in1: int, in2: int, in3: int, in4: int) -> None:
    super().__init__(name=name)
    self.IN1 = in1
    self.IN2 = in2
    self.IN3 = in3
    self.IN4 = in4
    self.__stepSleep = 0.004

    GPIO.setup(self.IN1, GPIO.OUT)
    GPIO.setup(self.IN2, GPIO.OUT)
    GPIO.setup(self.IN3, GPIO.OUT)
    GPIO.setup(self.IN4, GPIO.OUT)
  
  def setup(self):
    GPIO.setmode(GPIO.BCM)

  def tick(self):
    self.__stepForward(self.__stepSleep)
  
  def __stepForward(self, stepSleep):
    for i in range(4):
      if i%4==0:
        GPIO.output(self.IN4, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.LOW)
      elif i%4==1:
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN1, GPIO.LOW)
      elif i%4==2:
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.LOW)
      elif i%4==3:
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.HIGH)

      sleep(stepSleep)
  
  def setSpeed(self, speed):
    minSpeed = 0.003
    maxSpeed = 0.006
    x = speed * (maxSpeed - minSpeed) / 100
    self.__stepSleep = x + minSpeed
    self.print(f"Setting {self.name} speed: {self.__stepSleep}")