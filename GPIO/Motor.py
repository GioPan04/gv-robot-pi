import RPi.GPIO as GPIO  # type: ignore

class Motor:
  def __init__(self, step_pin: int, dir_pin: int, hrz = 500) -> None:
    self.dir_pin = dir_pin
    GPIO.setup(step_pin, GPIO.OUT)
    GPIO.setup(dir_pin, GPIO.OUT)
    self.pwm = GPIO.PWM(step_pin, hrz)
    self.farward()
  
  def start(self) -> None:
    self.pwm.start(50)
  
  def change_speed(self, hrz) -> None:
    self.pwm.ChangeFrequency(hrz)

  def stop(self) -> None:
    self.pwm.stop()
  
  def farward(self) -> None:
    GPIO.output(self.dir_pin, False)
  
  def backward(self) -> None:
    GPIO.output(self.dir_pin, True)
