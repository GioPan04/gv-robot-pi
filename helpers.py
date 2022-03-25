def constrain(value: int, min: int, max: int) -> int:
  if value < min:
    return min
  elif value < max:
    return value
  return max