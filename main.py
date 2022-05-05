from GPIO.Ultrasonic import Ultrasonic
import RPi.GPIO as GPIO # type: ignore
from helpers import calculate_speed
from core.distance_thread import DistanceThread
import config

# Pinout strategy:
# Sensor top: trig -> GPIO 4, echo -> GPIO 14
# Sensor middle: trig -> GPIO 17, echo -> GPIO 27
# Sensor bottom: trig -> GPIO 15, echo -> GPIO 18
# Motor left: step -> 2
# Motor right: step -> 3

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize external devices
motorL = GPIO.PWM(config.MOTOR_LEFT_PIN, 500)
motorR = GPIO.PWM(config.MOTOR_RIGHT_PIN, 500)
sensorT = Ultrasonic(config.SONIC_TOP_TRG_PIN, config.SONIC_TOP_ECH_PIN)
sensorM = Ultrasonic(config.SONIC_MDL_TRG_PIN, config.SONIC_MDL_ECH_PIN)
sensorB = Ultrasonic(config.SONIC_BTM_TRG_PIN, config.SONIC_BTM_ECH_PIN)

# Separated thread that endlessly read the sonic sensor and get the lower value
distance_thread = DistanceThread("Distance", [sensorT, sensorM, sensorB])

if __name__ == '__main__':
  distance_thread.start()
  motorL.start(50)
  motorR.start(50)

  # Run endlessly the motors, adjust the left and right speed by it's distance from the left wall
  try:
    while True:
      distance = distance_thread.distance
      (left, right) = calculate_speed(distance)
      motorL.ChangeFrequency(left)
      motorR.ChangeFrequency(right)

      print(f"Left: {left}Hz Right: {right}Hz Distance: {distance}cm")
  except KeyboardInterrupt: # Don't log ^C
    pass
  except Exception as e:
    print(e)
  finally:
    print("Killing")
    distance_thread.stop()
    GPIO.cleanup()
