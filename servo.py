from time import sleep
import RPi.GPIO as GPIO  # type: ignore
from GPIO.Servo import Servo

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
servo = Servo(13)

servo.move(90)
sleep(3)

servo.move(180)
sleep(3)

servo.move(0)
servo.stop()
GPIO.cleanup()