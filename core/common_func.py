import config
import RPi.GPIO as GPIO # type: ignore
from core.color_thread import ColorThread
from GPIO.Motor import Motor
from gpiozero import Servo # type: ignore
import GPIO.PCF8591 as ADC
from helpers import color_selector


def init(color_thread: ColorThread, motorL: Motor, motorR: Motor) -> None:
  GPIO.output(config.ACTION_LED, True)
  color_thread.start()
  motorL.start()
  motorR.start()

def close(color_thread: ColorThread, motorL: Motor, motorR: Motor, servo: Servo) -> None:
  GPIO.output(config.ACTION_LED, False)
  motorL.stop()
  motorR.stop()
  servo.close()
  color_thread.stop()
  GPIO.cleanup()
  exit(0)
