from GPIO.Motor import Motor
from time import sleep, time
import config
from helpers import calculate_speed

class Car:
  def __init__(self, left_motor: Motor, right_motor: Motor) -> None:
    self.left = left_motor
    self.right = right_motor
  
  def turn_left(self, secs=1.2, speed=500) -> None:
    self.left.backward()
    self.right.farward()
    self.left.change_speed(speed)
    self.right.change_speed(speed)
    sleep(secs)
  
  def turn_right(self, secs=1.2, speed=500) -> None:
    self.left.farward()
    self.right.backward()
    self.left.change_speed(speed)
    self.right.change_speed(speed)
    sleep(secs)
  
  def stop(self) -> None:
    self.left.change_speed(1)
    self.right.change_speed(1)
  
  def go_backward(self, secs: float, distance: int, callback, speed = config.BASE_SPEED, turning_speed = config.TURNING_SPEED) -> None:
    start = time()
    while start + secs > time():
      current_distance = callback()
      (left, right) = calculate_speed(current_distance, distance, speed, turning_speed)
      self.backward(right, left)
  
  def farward(self, speed: int) -> None:
    self.straight(speed, speed)
  
  def go(self, secs: float, distance: int, callback, speed = config.BASE_SPEED, turning_speed = config.TURNING_SPEED) -> None:
    start = time()
    while start + secs > time():
      current_distance = callback()
      (left, right) = calculate_speed(current_distance, distance, speed, turning_speed)
      self.straight(left, right)

  def backward(self, left_speed: int, right_speed: int) -> None:
    self.left.backward()
    self.right.backward()
    self.left.change_speed(left_speed)
    self.right.change_speed(right_speed)

  def straight(self, left_speed: int, right_speed: int) -> None:
    self.left.farward()
    self.right.farward()
    self.left.change_speed(left_speed)
    self.right.change_speed(right_speed)
