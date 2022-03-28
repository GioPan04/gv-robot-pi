from threading import Thread
import RPi.GPIO as GPIO

def constrain(value: int, min: int, max: int) -> int:
  """Constrain a value between two values"""
  if value < min:
    return min
  elif value < max:
    return value
  return max

# When the program exit cleanup the GPIO and stop the thread
def exit_handler(thread: Thread):
  print("Exiting...")
  GPIO.cleanup()
  thread.stop()