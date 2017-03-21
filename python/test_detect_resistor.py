import numpy as np
import cv2

COLORS = 'bg black greenbg blue brown green red'.split(' ')
color_samples = np.load('color_samples.npz')
samples = []
responses = []
for i, color in enumerate(COLORS):
  sample = color_samples[color]
  response = np.array([i]*sample.shape[0], dtype=np.int32)
  samples.append(sample)
  responses.append(response)
samples = np.concatenate(samples)
responses = np.concatenate(responses)

bgclass = cv2.NormalBayesClassifier(samples, responses)


