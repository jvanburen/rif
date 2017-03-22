import numpy as np
import cv2
import heapq

class Classifier:
  COLORS = 'bg black greenbg blue brown green red'.split(' ')
  BAND_COLORS = [(i, c) for (i, c) in enumerate(COLORS) if 'bg' not in c]
  output_buffer = np.empty((1024, 1024), dtype=bool)

  @staticmethod
  def scale_up(A, B):     # fill A with B scaled by 4
    k = 4
    X = Y = 1024
    shaped = B.reshape((256, 256))
    for y in range(k):
        for x in range(k):
            A[y:Y:k, x:X:k] = shaped

  @classmethod
  def segment_fg(cls, img):
    assert img.dtype == np.float32
    assert len(img.shape) in (2, 3) and img.shape[-1] == 3

    smol = img[::4, ::4, :]
    retcode, prediction = cls.bgclass.predict(smol.reshape(-1, 3))
    # Classifier.scale_up(Classifier.output_buffer, prediction)
    return prediction

  @classmethod
  def extract_resistor_bands(cls, image):
    fgbw8 = cls.segment_fg(image).astype(np.uint8).reshape((256, 256))*255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    opened = cv2.morphologyEx(fgbw8, cv2.MORPH_OPEN, kernel, iterations=5)
    _, contours, _ = cv2.findContours(opened, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
      print('no contours found!')
      cv2.imwrite('bad.png', fgbw8)
      cv2.imwrite('badopen.png', opened)
      return None
    biggest_contour = max(contours, key=cv2.contourArea)
    if cv2.contourArea(biggest_contour) < 800:
      print('no big contour found!', cv2.contourArea(biggest_contour))
      return None

    if cv2.contourArea(biggest_contour) > 2300:
      print('too big contour found!', cv2.contourArea(biggest_contour))
      return None

    biggest_contour *= 4 #scale up to original image

    M = cv2.moments(biggest_contour)
    centroid = int(M['m10']/M['m00']), int(M['m01']/M['m00']) #TODO: maybe swap???


    cimg = np.zeros(image.shape[0:2], dtype=np.uint8)
    cimg = cv2.drawContours(cimg, [biggest_contour], 0, color=255, thickness=-1)
    pts = np.stack(np.where(cimg == 255), -1)

    resistor_pixels = image[pts[:,0], pts[:,1], :]
    recode, responses = cls.colorclass.predict(resistor_pixels)
    responses = responses.ravel()
    #get list of (locations of pixels of color c, color c)
    color_responses = [(pts[np.where(responses == i), :].reshape(-1, 2), c) for i, c in cls.BAND_COLORS]

    most_colors = heapq.nlargest(3, color_responses, key=lambda x: len(x[0]))
    if not all(x[0].size for x in most_colors):
      print('not enough colors!', most_colors)
      # assert False
      return None

    centroids = [(sum(pts), c) for pts, c in most_colors]
    farthest, *others = sorted(centroids, key= lambda x: sum((x[0].astype(float) - centroid)**2), reverse=True)
    centroid = farthest[0]
    # def distance(x):
    #   new_centroid = (x.astype(float) - centroid.astype(float))


    others = sorted(others, key= lambda x: sum((x[0].astype(float) - centroid.astype(float))**2), reverse=False)
    bandcolors = [c for _, c in [farthest] + others]
    return bandcolors

    # keypoints = detector.detect(im)


def _load_classifiers(color_samples='color_samples.npz'):
  color_samples = np.load(color_samples)
  samples = []
  bgsamples = []
  responses = []
  bgresponses = []
  for i, color in enumerate(Classifier.COLORS):
    sample = color_samples[color]

    color_count = sample.shape[0]

    response = np.array([i]*color_count, dtype=np.int32)
    bgresponse = np.array([int(color != 'greenbg')] * color_count, dtype=np.int32)

    if color != 'greenbg':
      responses.append(response)
      samples.append(sample)
    bgsamples.append(sample)
    bgresponses.append(bgresponse)

  samples = np.concatenate(samples)
  bgsamples = np.concatenate(bgsamples)
  responses = np.concatenate(responses)
  bgresponses = np.concatenate(bgresponses)

  colorclass = cv2.ml.NormalBayesClassifier_create()
  colorclass.train(samples, cv2.ml.ROW_SAMPLE, responses)

  bgclass = cv2.ml.NormalBayesClassifier_create()
  bgclass.train(bgsamples, cv2.ml.ROW_SAMPLE, bgresponses)

  Classifier.colorclass = colorclass
  Classifier.bgclass = bgclass

_load_classifiers()
