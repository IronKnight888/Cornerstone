import cv2
import numpy as np
from config import lower_orange, upper_orange, lower_purple, upper_purple, kernel

def detect_color(frame, center, radius):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

    mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_OPEN, kernel)
    mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_DILATE, kernel)
    mask_purple = cv2.morphologyEx(mask_purple, cv2.MORPH_OPEN, kernel)
    mask_purple = cv2.morphologyEx(mask_purple, cv2.MORPH_DILATE, kernel)

    circle_mask = np.zeros_like(mask_orange)
    cv2.circle(circle_mask, center, radius, 255, -1)

    orange_zone = cv2.bitwise_and(mask_orange, mask_orange, mask=circle_mask)
    purple_zone = cv2.bitwise_and(mask_purple, mask_purple, mask=circle_mask)

    orange_pixels = cv2.countNonZero(orange_zone)
    purple_pixels = cv2.countNonZero(purple_zone)
    total_circle = np.count_nonzero(circle_mask)

    orange_detected = (orange_pixels / total_circle) >= 0.3
    purple_detected = (purple_pixels / total_circle) >= 0.3

    if orange_detected and purple_detected:
        return "PURPLE"  # prioritize purple
    elif orange_detected:
        return "ORANGE"
    elif purple_detected:
        return "PURPLE"
    else:
        return "NONE"
