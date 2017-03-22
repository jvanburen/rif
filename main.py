#!/usr/bin/env python3

VALUES = {'black': 0, 'blue': 6, 'brown': 1, 'green': 5, 'red': 2}
MULT = {'black': 1, 'blue': 1000000, 'brown': 10, 'green': 100000, 'red': 100}
def compute_resistance(bands):
  if bands is None: return None
  band1, band2, mult = reversed(bands)
  base =  VALUES[band1] * 10 + VALUES[band2]
  return base * MULT[mult]

from display import display
from camera import Camera
from classifier import Classifier

display.welcome_screen()

while 1:
  image = Camera.capture()
  bands = Classifier.extract_resistor_bands(image)
  print(bands)
  value = compute_resistance(bands)
  display.draw_resistance(value)

