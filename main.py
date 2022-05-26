from os import system
from GPIO.car import Car
import config
import RPi.GPIO as GPIO # type: ignore
from gpiozero import Servo # type: ignore
import GPIO.PCF8591 as ADC
from GPIO.Motor import Motor
from time import sleep, time
from core.logo import print_logo
from core.start_waiter import wait_start
from helpers import calculate_speed, color_selector
from core.color_thread import ColorThread
from gpiozero.pins.pigpio import PiGPIOFactory # type: ignore
from core.common_func import init, close

print_logo()

# Pinout strategy:
# Motor left: step -> 6, dir -> 13
# Motor right: step -> 19, dir -> 26
# Servo motor: data -> 12
# Start button: in -> 21

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ADC.setup(config.IR_ADDR)
factory = PiGPIOFactory()

GPIO.setup(config.ACTION_LED, GPIO.OUT)
motorL = Motor(config.MOTOR_LEFT_PIN, config.MOTOR_LEFT_DIR_PIN)
motorR = Motor(config.MOTOR_RIGHT_PIN, config.MOTOR_RIGHT_DIR_PIN)
car = Car(motorL, motorR)
servo = Servo(config.SERVO_PIN, pin_factory=factory, initial_value=-1)

# Read pixy colors in a separated thread
color_thread = ColorThread()

def get_distance_and_blocks() -> float:
  distance = ADC.read(config.IR_CHNL)
  color_selector(color_thread.color, servo)
  return distance

def get_abs_distance_and_blocks() -> float:
  distanceT = ADC.read(config.IR_CHNL)
  distanceB = ADC.read(config.IR_CHNL)
  color_selector(color_thread.color, servo)
  return distanceT - distanceB

if __name__ == '__main__':
  if(not config.DEBUG):
    wait_start()
  init(color_thread, motorL, motorR)
  started = time()

  try:
    car.farward(150)
    sleep(1)

    # Turn left
    car.turn_left()

    # Wait 0.5 seconds
    car.stop()
    sleep(0.5)

    car.go(7, 78, lambda: ADC.read(config.IR_CHNL), config.BASE_SPEED + 200)
    car.turn_right()

    car.go(53, 135, get_distance_and_blocks)
    car.turn_right(1.3)

    car.go(29, 0, get_abs_distance_and_blocks)
    car.turn_right(1.2)

    car.go(55.5, 135, get_distance_and_blocks)
    car.turn_right(1.3)

    while True:
      distance = ADC.read(config.IR_CHNL)
      (left, right) = calculate_speed(distance, 135, config.BASE_SPEED, config.TURNING_SPEED)
      car.straight(left, right)

  except KeyboardInterrupt: # Don't log ^C
    pass
  except Exception as e:
    print(e)
  finally:
    print("Killing")
    print(f"Time: {time() - started}")
    close(color_thread, motorL, motorR, servo)