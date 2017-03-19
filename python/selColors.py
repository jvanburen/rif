import cv2
import numpy as np

def selColors(img):
  lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
  L = lab[:, :, 0]
  A = lab[:, :, 1]
  B = lab[:, :, 2]

  # grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  # gaussian = cv2.GaussianBlur(grey,(5,5),5)
  # laplacian = cv2.Laplacian(A,cv2.CV_64F)

  # bayesInput = np.dstack([lab, laplacian])
  # sobelx = cv2.Sobel(A,cv2.CV_64F,1,0,ksize=5)
  # sobely = cv2.Sobel(gaussian,cv2.CV_64F,0,1,ksize=5)

  # sqrtthing = np.sqrt(np.square(sobelx)+np.square(sobely))

  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
  fgbg = cv2.createBackgroundSubtractorGMG()

  fgmask = fgbg.apply(lab)
  fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
  cv2.imshow('frame',fgmask)


I = cv2.imread('resistor.png')
selColors(I)