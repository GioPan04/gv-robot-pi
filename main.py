from GPIO.Motor import Motor
import RPi.GPIO as GPIO  # type: ignore
from helpers import calculate_speed
from core.color_thread import ColorThread
import config
import GPIO.PCF8591 as ADC
from gpiozero import Servo # type: ignore
from gpiozero.pins.pigpio import PiGPIOFactory # type: ignore
factory = PiGPIOFactory()

# Pinout strategy:
# Sensor top: trig -> GPIO 4, echo -> GPIO 14
# Sensor middle: trig -> GPIO 17, echo -> GPIO 27
# Sensor bottom: trig -> GPIO 15, echo -> GPIO 18
# Motor left: step -> 2
# Motor right: step -> 3
# Servo motor: data -> 13

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(config.MOTOR_LEFT_PIN, GPIO.OUT)
GPIO.setup(config.MOTOR_RIGHT_PIN, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, True)

# Initialize external devices
motorL = Motor(config.MOTOR_LEFT_PIN)
motorR = Motor(config.MOTOR_RIGHT_PIN)
servo = Servo(config.SERVO_PIN, pin_factory=factory, initial_value=-1)

# Separated thread that endlessly read the sonic sensor and get the lower value
color_thread = ColorThread("Colors")

ADC.setup(0x48)

if __name__ == '__main__':
  #distance_thread.start()
  color_thread.start()
  motorL.start()
  motorR.start()

  # Run endlessly the motors, adjust the left and right speed by it's distance from the left wall
  try:
    while True:
      #distance = distance_thread.distance
      distance = ADC.read(2)
      (left, right) = calculate_speed(distance)
      motorL.change_speed(left)
      motorR.change_speed(right)

      if(color_thread.color == 3):
        servo.value = 0.2
      else:
        servo.min()

      # print(f"Left: {left}Hz Right: {right}Hz Distance: {distance}cm")
  except KeyboardInterrupt: # Don't log ^C
    pass
  except Exception as e:
    print(e)
  finally:
    print("Killing")
    motorL.stop()
    motorR.stop()
    servo.stop()
    color_thread.stop()
    GPIO.cleanup()
