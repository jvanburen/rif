#!/usr/bin/env python3
import picamera
import numpy as np
import cv2
import time
import atexit

if __name__ == '__main__':
  print("Don't run this")
  exit(1)

class Camera:
  imagebuffer = np.empty((1024, 1024, 3,), dtype=np.uint8, order='C')
  camera = picamera.PiCamera()
  camera.resolution = (1024, 1024)
  camera.zoom = (730/2592, 440/1944, 1024/2592, 1024/1944)
  camera.iso = 100
  camera.shutter_speed = 29984
  time.sleep(5) # gotta wait for it to adjust

  @classmethod
  def capture(cls):
    cls.camera.capture(np.ravel(cls.imagebuffer), 'bgr')
    normalizedimg = cls.imagebuffer.astype(np.float32) / 255
    return cv2.cvtColor(normalizedimg, cv2.COLOR_BGR2Lab)

  @classmethod
  def close(cls):
    cls.camera.close()

atexit.register(Camera.close)

