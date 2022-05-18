from core.base_thread import BaseThread
from core.pixy.pixy import *
import core.pixy.pixy as pixy
import config

class ColorThread(BaseThread):
  def __init__(self, name: str, colors_length = 5) -> None:
    super().__init__(name=name)
    self.color = None
    self.last_color = None
    self.__colors_length = colors_length
    self.__blocks = BlockArray(self.__colors_length)
    self.__blocks_count = 0

  def setup(self):
    pixy.init()
    pixy.change_prog("color_connected_components")

  def tick(self):
    self.__blocks_count = pixy.ccc_get_blocks(self.__colors_length, self.__blocks)
    if(self.__blocks_count > 0):
      self.color = self.__blocks[0].m_signature
      self.last_color = self.color
    else:
      self.color = None

    