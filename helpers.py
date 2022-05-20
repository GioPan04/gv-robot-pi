import config

def constrain(value: int, min: int, max: int) -> int:
  """Constrain a value between two values"""
  if value < min:
    return min
  elif value < max:
    return value
  return max

def calculate_speed(current_distance: float, distance: float, base_speed: float, turning_speed: float) -> tuple[int, int]:
  right = base_speed
  left = base_speed

  if(current_distance >= distance):
    left += turning_speed
    right -= turning_speed
  else:
    right += turning_speed
    left -= turning_speed

  return left, right

def color_selector(color: int, servo, closed = -0.7, opened = 0.2):
  """Open the servo only when a whitelisted color is detected"""
  if(color in config.BLOCKS_WHITELIST):
    servo.value = opened
  else:
    servo.value = closed