import RPi.GPIO as GPIO  # type: ignore

class Motor:
  def __init__(self, dir_pin: int, hrz = 500) -> None:
    self.dir_pin = dir_pin
    GPIO.setup(dir_pin, GPIO.OUT)
    self.pwm = GPIO.PWM(dir_pin, hrz)
  
  def start(self) -> None:
    self.pwm.start(50)
  
  def change_speed(self, hrz) -> None:
    self.pwm.ChangeFrequency(hrz)

  def stop(self) -> None:
    self.pwm.stop()
