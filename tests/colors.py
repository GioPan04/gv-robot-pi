from ctypes import *
from pixy import *
import pixy

pixy.init()
pixy.change_prog("color_connected_components")

class Block (Structure):
  _fields_ = [
    ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint)
  ]

blocks = BlockArray(10)

COLORS = {
  1: "yellow",
  2: "blue",
  3: "green"
}

while True:
  count = pixy.ccc_get_blocks(10, blocks)
  if(count > 0):
    color = blocks[0].m_signature
    print(f"Found {COLORS[color]}")
