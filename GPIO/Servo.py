import RPi.GPIO as GPIO  # type: ignore

class Servo:
  def __init__(self, pin: int) -> None:
    GPIO.setup(pin, GPIO.OUT)
    self.servo = GPIO.PWM(pin, 50)
    self.servo.start(0)
  
  def move(self, angle: int) -> None:
    duty = angle / 18 + 2
    self.servo.ChangeDutyCycle(duty)
    