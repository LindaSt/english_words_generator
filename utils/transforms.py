# from https://github.com/tensorflow/models/blob/master/research/autoaugment/augmentation_transforms.py

import random
from PIL import Image
import numpy as np


def shear_x(pil_img, level):
    """Applies PIL ShearX to `pil_img`.
  The ShearX operation shears the image along the horizontal axis with `level`
  magnitude.
  Args:
    pil_img: Image in PIL object.
    level: Strength of the operation specified as an Integer from
      [0, `PARAMETER_MAX`].
  Returns:
    A PIL Image that has had ShearX applied to it.
  """
    i, j = np.random.uniform(low=1-level, high=1+level, size=2)
    if random.random() > 0.5:
        level = -level
    return pil_img.transform(pil_img.size, Image.AFFINE, (i, level, 0, 0, j, 0), fillcolor=255)


def shear_y(pil_img, level):
    """Applies PIL ShearY to `pil_img`.
  The ShearY operation shears the image along the vertical axis with `level`
  magnitude.
  Args:
    pil_img: Image in PIL object.
    level: Strength of the operation specified as an Integer from
      [0, `PARAMETER_MAX`].
  Returns:
    A PIL Image that has had ShearY applied to it.
  """
    i, j = np.random.uniform(low=1-level, high=1+level, size=2)
    if random.random() > 0.5:
        level = -level
    return pil_img.transform(pil_img.size, Image.AFFINE, (i, 0, 0, level, j, 0), fillcolor=255)

