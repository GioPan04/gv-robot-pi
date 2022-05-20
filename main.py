import config
import RPi.GPIO as GPIO # type: ignore
from gpiozero import Servo # type: ignore
import GPIO.PCF8591 as ADC
from GPIO.Motor import Motor
from time import sleep, time
from helpers import calculate_speed, color_selector
from core.ansicolors import AnsiColors  # type: ignore
from core.color_thread import ColorThread
from gpiozero.pins.pigpio import PiGPIOFactory # type: ignore

logo = open("./logo.txt", "r")
print(AnsiColors.OKBLUE + AnsiColors.BOLD + logo.read() + AnsiColors.ENDC + "\n")
logo.close()


# Pinout strategy:
# Motor left: step -> 6, dir -> 13
# Motor right: step -> 19, dir -> 26
# Servo motor: data -> 12

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ADC.setup(config.IR_ADDR)
factory = PiGPIOFactory()

motorL = Motor(config.MOTOR_LEFT_PIN, config.MOTOR_LEFT_DIR_PIN)
motorR = Motor(config.MOTOR_RIGHT_PIN, config.MOTOR_RIGHT_DIR_PIN)
servo = Servo(config.SERVO_PIN, pin_factory=factory, initial_value=-1)

# Read pixy colors in a separated thread
color_thread = ColorThread()

def init() -> None:
  color_thread.start()
  motorL.start()
  motorR.start()

def close() -> None:
  motorL.stop()
  motorR.stop()
  servo.close()
  color_thread.stop()
  GPIO.cleanup()
  exit(0)

if __name__ == '__main__':
  init()

  try:
    motorL.change_speed(150)
    motorR.change_speed(150)
    sleep(1)

    # Turn left
    motorL.backward()
    motorR.farward()
    motorL.change_speed(500)
    motorR.change_speed(500)
    sleep(1.2)

    # Wait 0.5 seconds
    motorR.change_speed(1)
    motorL.change_speed(1)
    sleep(0.5)

    # Go farward for 7 seconds and stay straight
    motorL.farward()
    motorR.farward()

    initial = time()
    while initial + 7 > time():
      distance = ADC.read(config.IR_CHNL)
      (left, right) = calculate_speed(distance, 78, config.BASE_SPEED + 200, config.TURNING_SPEED)
      motorL.change_speed(left)
      motorR.change_speed(right)
    
    # Turn right
    motorL.farward()
    motorR.backward()
    motorL.change_speed(500)
    motorR.change_speed(500)
    sleep(1.2)

    motorL.farward()
    motorR.farward()

  # Go farward forever and stay straight
    while True:
      distance = ADC.read(config.IR_CHNL)
      (left, right) = calculate_speed(distance, 135, config.BASE_SPEED, config.TURNING_SPEED)
      motorL.change_speed(left)
      motorR.change_speed(right)
      
      color_selector(color_thread.color, servo)
      # print(f"Left: {left}Hz Right: {right}Hz Distance: {distance}cm")

  except KeyboardInterrupt: # Don't log ^C
    pass
  except Exception as e:
    print(e)
  finally:
    print("Killing")
    close()