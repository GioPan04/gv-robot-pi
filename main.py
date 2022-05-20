from GPIO.Motor import Motor
import RPi.GPIO as GPIO
from core.ansicolors import AnsiColors  # type: ignore
from helpers import calculate_speed
from core.color_thread import ColorThread
import config
import GPIO.PCF8591 as ADC
from gpiozero import Servo # type: ignore
from gpiozero.pins.pigpio import PiGPIOFactory # type: ignore
from time import sleep, time

logo = open("./logo.txt", "r")
print(AnsiColors.OKBLUE + AnsiColors.BOLD + logo.read() + AnsiColors.ENDC + "\n")
logo.close()

factory = PiGPIOFactory()

# Pinout strategy:
# Motor left: step -> 6, dir -> 13
# Motor right: step -> 19, dir -> 26
# Servo motor: data -> 12

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ADC.setup(0x48)

motorL = Motor(config.MOTOR_LEFT_PIN, config.MOTOR_LEFT_DIR_PIN)
motorR = Motor(config.MOTOR_RIGHT_PIN, config.MOTOR_RIGHT_DIR_PIN)
servo = Servo(config.SERVO_PIN, pin_factory=factory, initial_value=-1)

# Read pixy colors in a separated thread
color_thread = ColorThread()

if __name__ == '__main__':
  color_thread.start()
  motorL.start()
  motorR.start()

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

    # Go farward for 7 seconds and go straight
    motorL.farward()
    motorR.farward()

    initial = time()
    while initial + 7 > time():
      distance = ADC.read(2)
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

  # Run endlessly the motors, adjust the left and right speed by it's distance from the left wall
    while True:
      distance = ADC.read(2)
      (left, right) = calculate_speed(distance, 135, config.BASE_SPEED, config.TURNING_SPEED)
      motorL.change_speed(left)
      motorR.change_speed(right)

      if(color_thread.color == 1):
        servo.value = 0.2
      else:
        servo.value = -0.7

      # print(f"Left: {left}Hz Right: {right}Hz Distance: {distance}cm")
  except KeyboardInterrupt: # Don't log ^C
    pass
  except Exception as e:
    print(e)
  finally:
    print("Killing")
    motorL.stop()
    motorR.stop()
    color_thread.stop()
    GPIO.cleanup()
