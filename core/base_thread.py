from threading import Thread
from core.ansicolors import AnsiColors

class BaseThread(Thread):
  def __init__(self, name: str) -> None:
    super().__init__(name=name)
    self._run = True
  
  def print(self, message: str) -> None:
    print(f"[{AnsiColors.OKGREEN}{self.name}{AnsiColors.ENDC}]: {message}")
  
  def setup(self):
    pass

  def tick(self):
    pass

  def run(self):
    self.setup()
    while self._run:
      self.tick()
    
    self.print("Thread stopped")
  
  def stop(self):
    self._run = False
    self.print("Stopping thread")
    self.join()
