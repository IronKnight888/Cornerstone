import cv2
import time
import numpy as np
from config import lower_orange, upper_orange, lower_purple, upper_purple, kernel
from color_detection import detect_color
from arduino_input import connect_arduino, wait_for_button
from powerpoint_control import go_to_slide
from questions import TRACK_1_QUESTIONS
import random

track_0_slides = [
    2, 3, 25,
    (26, 27, 28), (30, 29), (31, 32),
    33, (34, 35, 36), (38, 37), (39, 40),
    41, (42, 43, 44), (46, 45), (47, 48),
    49, (50, 51, 52), (54, 53), (55, 56),
    57, (58, 59, 60), (62, 61), (63, 64)
]

track_2_slides = [
    2, 3, 25, (26, 27, 28), (30, 29), (31, 32), 33, (34, 35, 36), (38, 37), (39, 40),
     41, (42, 43, 44), (46, 45), (47, 48), 49, (50, 51, 52), (54, 53), (55, 56),
     57, (58, 59, 60), (62, 61), (63, 64)
     
]

track_3_slides = [  
    2, 3, 115, (116, 117, 118), (119, 120), (121, 122), 123, (124, 125, 126), (127, 128), (129, 130),
     131, (132, 133, 134), (135, 136), (137, 138), 139, (140, 141, 142), (143, 144), (145, 146),
     147, (148, 149, 150), (151, 152), (153, 154)
     
]
    
track_4_slides = [      
    2, 3, 160, (161, 162, 163), (164, 165), (166, 167), 168, (169, 170, 171), (172, 173), (174, 175),
     176, (177, 178, 179), (180, 181), (182, 183), 184, (185, 186, 187), (188, 189), (190, 191),
     192, (193, 194, 195), (196, 197), (198, 199)
]

track_1_slides = random.choice([track_0_slides, track_2_slides, track_3_slides, track_4_slides])

print(track_1_slides)