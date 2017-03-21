import numpy as np
import cv2

class Classifier:
  COLORS = 'bg black greenbg blue brown green red'.split(' ')
  def __init__(self, color_samples='color_samples.npz'):
    color_samples = np.load(color_samples)
    samples = []
    responses = []
    bgresponses = []
    count = 0
    for i, color in enumerate(Classifier.COLORS):
      sample = color_samples[color]
      samples.append(sample)

      color_count = sample.shape[0]
      count += color_count

      response = np.array([i]*color_count, dtype=np.int32)
      bgresponse = np.array([int(color != 'greenbg')] * color_count, dtype=np.int32)
      responses.append(response)
      bgresponses.append(bgresponse)

    samples = np.concatenate(samples)
    responses = np.concatenate(responses)
    bgresponses = np.concatenate(bgresponses)

    colorclass = bgclass = cv2.ml.NormalBayesClassifier_create()
    colorclass.train(samples, cv2.ml.ROW_SAMPLE, responses)

    bgclass = cv2.ml.NormalBayesClassifier_create()
    bgclass.train(samples, cv2.ml.ROW_SAMPLE, bgresponses)

    self.colorclass = colorclass
    self.bgclass = bgclass



