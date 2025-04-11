import numpy as np

# Calibrated HSV ranges from actual object tests
lower_orange = np.array([0, 40, 40])
upper_orange = np.array([40, 255, 255])

lower_purple = np.array([90, 40, 40])
upper_purple = np.array([130, 255, 255])

kernel = np.ones((5, 5), np.uint8)