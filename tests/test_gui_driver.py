import pytest
import sys

sys.path.append('gui')

from gui_driver import GUIDriver

GLOBAL_GUI_WIDTH = 500
GLOBAL_GUI_HEIGHT = 1000
GLOBAL_GUI_DRIVER = GUIDriver(None, GLOBAL_GUI_WIDTH, GLOBAL_GUI_HEIGHT)

def test_gui_driver_init():
  # Test gui_driver properties
  assert GLOBAL_GUI_DRIVER.parent is None
  assert GLOBAL_GUI_DRIVER.window_width == GLOBAL_GUI_WIDTH
  assert GLOBAL_GUI_DRIVER.window_height == GLOBAL_GUI_HEIGHT

  # test gui_driver frames
  assert GLOBAL_GUI_DRIVER.frames['infoFrame']['width'] == 200 
  assert GLOBAL_GUI_DRIVER.frames['infoFrame']['height'] == 1000

  assert GLOBAL_GUI_DRIVER.frames['databaseFrame']['width'] == 50
  assert GLOBAL_GUI_DRIVER.frames['databaseFrame']['height'] == 400

  assert GLOBAL_GUI_DRIVER.frames['parameterFrame']['width'] == 250
  assert GLOBAL_GUI_DRIVER.frames['parameterFrame']['height'] == 400

  assert GLOBAL_GUI_DRIVER.frames['orderFrame']['width'] == 300
  assert GLOBAL_GUI_DRIVER.frames['orderFrame']['height'] == 50

  assert GLOBAL_GUI_DRIVER.frames['jobsFrame']['width'] == 300
  assert GLOBAL_GUI_DRIVER.frames['jobsFrame']['height'] == 550
