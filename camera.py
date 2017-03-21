import picamera
import numpy as np
import time

with picamera.PiCamera() as camera:
    camera.zoom = (730/2592, 440/1944, 1024/2592, 1024/1944)
    time.sleep(2)
    image = np.empty((1024 * 1024 * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((1024, 1024, 3))

