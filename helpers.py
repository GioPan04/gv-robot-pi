import config

def constrain(value: int, min: int, max: int) -> int:
  """Constrain a value between two values"""
  if value < min:
    return min
  elif value < max:
    return value
  return max

def calculate_speed(distance: float) -> tuple[int, int]:
  right = config.BASE_SPEED
  left = config.BASE_SPEED

  if(distance > config.DISTANCE):
    right += config.TURNING_SPEED
  else:
    left += config.TURNING_SPEED

  return left, right
