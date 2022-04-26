from time import sleep
from GPIO.Motor import Motor
import RPi.GPIO as GPIO # type: ignore

def test():
  GPIO.setmode(GPIO.BCM)

  motor = Motor("Motor", 6, 13, 19, 26)

  motor.start()

  sleep(10)

  motor.setSpeed(0)

  sleep(3)

  motor.setSpeed(100)

  sleep(3)

  motor.setSpeed(5)

  sleep(3)

  motor.stop()

  GPIO.cleanup()