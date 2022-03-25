import RPi.GPIO as GPIO
import time

class Ultrasonic(object):
  def __init__(self, trig, echo):
    self.trig = trig
    self.echo = echo
    
    GPIO.setup(trig, GPIO.OUT)
    GPIO.output(trig, 0)
    GPIO.setup(echo, GPIO.IN)
  
  def measure(self):
    GPIO.output(self.trig, 1)
    time.sleep(0.00001)
    GPIO.output(self.trig, 0)

    while GPIO.input(self.echo) == 0:
      pass
    
    start = time.time()
    while GPIO.input(self.echo) == 1:
      pass
    stop = time.time()

    return (stop - start) * 17000
    