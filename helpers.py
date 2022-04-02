import config
import RPi.GPIO as GPIO
from core.distance_thread import DistanceThread

def constrain(value: int, min: int, max: int) -> int:
  """Constrain a value between two values"""
  if value < min:
    return min
  elif value < max:
    return value
  return max

def calculate_speed(distance: float) -> tuple[int, int]:
  speed = config.K * (distance - config.DISTANCE)
  right = constrain(config.BASE_SPEED + speed, config.MIN_SPEED, config.MAX_SPEED)
  left = constrain(config.BASE_SPEED - speed, config.MIN_SPEED, config.MAX_SPEED)

  return left, right
