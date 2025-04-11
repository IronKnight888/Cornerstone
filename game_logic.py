import cv2
import time
import numpy as np
import random
from config import lower_orange, upper_orange, lower_purple, upper_purple, kernel
from color_detection import detect_color
from arduino_input import connect_arduino, wait_for_button
from powerpoint_control import go_to_slide
from questions import TRACK_1_QUESTIONS

# Random seed
random.seed(time.time())

# --- TRACKS ---
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

# Select a random track
selected_track_slides = random.choice([track_0_slides, track_2_slides, track_3_slides, track_4_slides])
print("🎲 Selected Track:", selected_track_slides[:6], "...")

# Indices where detection slides occur
DETECTION_SLIDE_INDICES = [3, 7, 11, 15, 19]

# Get valid detection tuples from selected track
detection_tuples = [
    slide for i, slide in enumerate(selected_track_slides)
    if i in DETECTION_SLIDE_INDICES and isinstance(slide, tuple) and len(slide) == 3
]

CIRCLE_POSITIONS = [
    (0.32, 0.48),
    (0.40, 0.33),
    (0.76, 0.44),
    (0.55, 0.44),
    (0.70, 0.61),
]


def start_game_loop():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS, 15)

    if not cap.isOpened():
        print("🚨 Camera failed to open.")
        return

    ser = connect_arduino()

    while True:
        go_to_slide(1)
        print("📍 Waiting for Arduino button to start...")

        while True:
            if wait_for_button(ser):
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                ser.close()
                cv2.destroyAllWindows()
                return

        play_game(cap, ser, selected_track_slides, detection_tuples)


def play_game(cap, ser, slides, detection_tuples):
    questions = TRACK_1_QUESTIONS
    score = 50
    decision_index = 0
    i = 0
    choice = None  # Initialize here for safety

    while i < len(slides):
        current = slides[i]

        if isinstance(current, tuple) and len(current) == 3 and current in detection_tuples:
            print(f"🎯 Starting decision {decision_index + 1} at slides {current}")
            go_to_slide(current[2])  # Start on NONE
            detected_color = "NONE"
            frame_count = 0
            ser.reset_input_buffer()

            cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)
            cv2.moveWindow("Camera Feed", 100, 100)

            while True:
                ret, frame = cap.read()
                if not ret:
                    continue

                if frame_count % 2 != 0:
                    frame_count += 1
                    continue

                frame = cv2.rotate(frame, cv2.ROTATE_180)
                frame = cv2.resize(frame, (640, 480))

                h, w = frame.shape[:2]
                px, py = CIRCLE_POSITIONS[decision_index]
                center = (int(px * w), int(py * h))
                radius = 60
                cv2.circle(frame, center, radius, (0, 0, 255), 3)
                cv2.imshow("Camera Feed", frame)

                color = detect_color(frame, center, radius)

                if frame_count % 10 == 0:
                    emoji = {"PURPLE": "🟣", "ORANGE": "🟠", "NONE": "⚪"}.get(color, "❓")
                    print(f"{emoji} Detected: {color}")

                if color != detected_color:
                    slide_to_show = {
                        "PURPLE": current[0],
                        "ORANGE": current[1],
                        "NONE": current[2]
                    }.get(color, current[2])
                    go_to_slide(slide_to_show)
                    detected_color = color

                if color in ["ORANGE", "PURPLE"] and wait_for_button(ser):
                    choice = 1 if color == "ORANGE" else 0
                    i += 1
                    decision_index += 1
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return

                frame_count += 1

        elif isinstance(current, tuple) and len(current) == 2:
            selected_slide = current[choice]
            go_to_slide(selected_slide)
            print(f"➡️ Showing answer result: slide {selected_slide}")
            time.sleep(5)
            i += 1

        elif i > 0 and isinstance(slides[i - 1], tuple) and len(slides[i - 1]) == 2 and isinstance(current, tuple) and len(current) == 2:
            selected_text, result = questions[decision_index - 1][choice]
            correct = result > 0
            feedback_slide = current[0 if correct else 1]
            go_to_slide(feedback_slide)
            print(f"{'✅' if correct else '❌'} Feedback slide: {feedback_slide}")
            score += result
            print(f"🎯 Score updated: {score}")
            time.sleep(4)
            i += 1

        else:
            go_to_slide(current)
            time.sleep(5)
            i += 1

    final_slide = max(6, min(16, 6 + (score // 10)))
    go_to_slide(final_slide)
    print(f"🏁 Final Score: {score} → Slide {final_slide}")
    time.sleep(6)
