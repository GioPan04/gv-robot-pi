from GPIO.Motor import Motor
from GPIO.Servo import Servo
import RPi.GPIO as GPIO  # type: ignore
from GPIO.Ultrasonic import Ultrasonic
from helpers import calculate_speed
from core.distance_thread import DistanceThread
from core.color_thread import ColorThread
import config

# Pinout strategy:
# Sensor top: trig -> GPIO 4, echo -> GPIO 14
# Sensor middle: trig -> GPIO 17, echo -> GPIO 27
# Sensor bottom: trig -> GPIO 15, echo -> GPIO 18
# Motor left: step -> 2
# Motor right: step -> 3
# Servo motor: data -> 23

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.MOTOR_LEFT_PIN, GPIO.OUT)
GPIO.setup(config.MOTOR_RIGHT_PIN, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, True)
GPIO.setwarnings(False)

# Initialize external devices
motorL = Motor(config.MOTOR_LEFT_PIN)
motorR = Motor(config.MOTOR_RIGHT_PIN)
sensorT = Ultrasonic(config.SONIC_TOP_TRG_PIN, config.SONIC_TOP_ECH_PIN)
sensorM = Ultrasonic(config.SONIC_MDL_TRG_PIN, config.SONIC_MDL_ECH_PIN)
sensorB = Ultrasonic(config.SONIC_BTM_TRG_PIN, config.SONIC_BTM_ECH_PIN)
servo = Servo(config.SERVO_PIN)

# Separated thread that endlessly read the sonic sensor and get the lower value
distance_thread = DistanceThread("Distance", [sensorT, sensorM, sensorB])
color_thread = ColorThread("Colors")

if __name__ == '__main__':
  distance_thread.start()
  color_thread.start()
  motorL.start()
  motorR.start()

  # Run endlessly the motors, adjust the left and right speed by it's distance from the left wall
  try:
    while True:
      distance = distance_thread.distance
      (left, right) = calculate_speed(distance)
      motorL.change_speed(left)
      motorR.change_speed(right)

      # print(f"Left: {left}Hz Right: {right}Hz Distance: {distance}cm")
  except KeyboardInterrupt: # Don't log ^C
    pass
  except Exception as e:
    print(e)
  finally:
    print("Killing")
    color_thread.stop()
    distance_thread.stop()
    GPIO.cleanup()
