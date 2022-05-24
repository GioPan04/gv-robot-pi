from os import system
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
servo = Servo(config.SERVO_PIN, pin_factory=factory, initial_value=-1)

# Read pixy colors in a separated thread
color_thread = ColorThread()

def init() -> None:
  GPIO.output(config.ACTION_LED, True)
  color_thread.start()
  motorL.start()
  motorR.start()

def close() -> None:
  GPIO.output(config.ACTION_LED, False)
  motorL.stop()
  motorR.stop()
  servo.close()
  color_thread.stop()
  GPIO.cleanup()
  exit(0)

if __name__ == '__main__':
  if(not config.DEBUG):
    wait_start()
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

    top_distance = ADC.read(3)
  # Go farward forever and stay straight
    while(not ( top_distance > 20 and top_distance < 30)):

      distance = ADC.read(config.IR_CHNL)
      (left, right) = calculate_speed(distance, 135, config.BASE_SPEED, config.TURNING_SPEED)
      motorL.change_speed(left)
      motorR.change_speed(right)
      
      color_selector(color_thread.color, servo)
      # print(f"Left: {left}Hz Right: {right}Hz Distance: {distance}cm")

      top_distance = ADC.read(3)

      if(not config.DEBUG and not GPIO.input(config.START_BTN)):
        system('poweroff')
  

    # Turn right
    motorL.farward()
    motorR.backward()
    motorL.change_speed(500)
    motorR.change_speed(500)
    sleep(1.2)

    while True:
      distance = ADC.read(config.IR_CHNL)
      (left, right) = calculate_speed(distance, 28, config.BASE_SPEED, config.TURNING_SPEED)
      motorL.change_speed(left)
      motorR.change_speed(right)
      
      color_selector(color_thread.color, servo)

  except KeyboardInterrupt: # Don't log ^C
    pass
  except Exception as e:
    print(e)
  finally:
    print("Killing")
    close()