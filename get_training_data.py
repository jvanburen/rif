#!/usr/bin/env python
from __future__ import print_function, division

import cv2
import numpy as np
import os

COLORS = 'bg black greenbg blue brown green red'.split(' ')
num_pixels =  {'greenbg' : 1009922.2
              ,'black' : 1828.75
              ,'blue' : 2094.0
              ,'brown' : 2283.2
              ,'green' : 2353.25
              ,'red' : 2107.3333333333335
              ,'bg' : 27987.26666666672
              }
TOTAL_SAMPLES = 30000

SAMPLES_PER_PIXEL = float(TOTAL_SAMPLES)/(1024 * 1024)


def get_good_values(imagepath):
  "load image and filter out transparent values"
  print('loading', imagepath)
  image = cv2.imread(imagepath, cv2.IMREAD_UNCHANGED)
  if image.shape[-1] > 3:
    bw = image[:,:,3] >= 255
    cutout = image[bw][:,:3]
    img = cutout.reshape((1,-1,3))
  else:
    img = image
  img = (img / 255.0).astype(np.float32)

  return cv2.cvtColor(img, cv2.COLOR_BGR2Lab).reshape((-1, 3))

def load_color(color):
  fns = os.listdir(color)
  fns = [os.path.join(color, fn) for fn in fns if fn.endswith('.png')]
  color_arrs = [get_good_values(fn) for fn in fns]
  return np.concatenate(color_arrs)

def load_colors(colors=COLORS):
  color_arrs = {color : load_color(color) for color in colors}
  return color_arrs

def create_training_data(colors, file='color_samples.npz'):
  samples = {}
  for color in COLORS:
    num_samples = int(round(SAMPLES_PER_PIXEL * num_pixels[color]))
    pixel_values = colors[color]
    Npixels = pixel_values.size // 3
    rando_indices = np.random.choice(Npixels, size=num_samples, replace=False)
    samples[color] = pixel_values[rando_indices, :]
  if file:
    np.savez(file, **samples)
  return samples


if __name__ == '__main__':
  print(SAMPLES_PER_PIXEL , "SAMPLES_PER_PIXEL")
  colors = load_colors()
  arrays = create_training_data(colors)
  print("Created",
    sum(v.shape[0] for _, v in arrays.items()),
    "samples out of",
    sum(v.shape[0] for _, v in colors.items()))
