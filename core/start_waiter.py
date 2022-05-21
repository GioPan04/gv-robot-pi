import config
from time import time
import RPi.GPIO as GPIO # type: ignore

def wait_start() -> None:
  print("Press start button to start")
  GPIO.setup(config.START_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  while GPIO.input(config.START_BTN):
    if(int(time()) % 2 == 0):
      GPIO.output(config.ACTION_LED, True)
    else:
      GPIO.output(config.ACTION_LED, False)

  GPIO.output(config.ACTION_LED, False)
  print("Start button pressed, starting robot")