import cv2
import numpy as np
from config import lower_orange, upper_orange, lower_purple, upper_purple, kernel

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 15)

print("🔍 Starting live color debug. Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    height, width = hsv.shape[:2]
    center = (width // 2, height // 2)
    radius = 30
    circle_mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(circle_mask, center, radius, 255, -1)

    masked_hsv = cv2.bitwise_and(hsv, hsv, mask=circle_mask)
    mean_h = np.mean(hsv[:, :, 0][circle_mask == 255])
    mean_s = np.mean(hsv[:, :, 1][circle_mask == 255])
    mean_v = np.mean(hsv[:, :, 2][circle_mask == 255])

    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

    orange_zone = cv2.bitwise_and(mask_orange, mask_orange, mask=circle_mask)
    purple_zone = cv2.bitwise_and(mask_purple, mask_purple, mask=circle_mask)

    orange_pixels = cv2.countNonZero(orange_zone)
    purple_pixels = cv2.countNonZero(purple_zone)
    total_circle = np.count_nonzero(circle_mask)

    orange_detected = (orange_pixels / total_circle) >= 0.3
    purple_detected = (purple_pixels / total_circle) >= 0.3

    if orange_detected:
        color_status = "🟠 ORANGE"
    elif purple_detected:
        color_status = "🟣 PURPLE"
    else:
        color_status = "⚪ NONE"

    # Display status
    print(f"HSV Mean in Circle → H: {mean_h:.1f}, S: {mean_s:.1f}, V: {mean_v:.1f} → Detected: {color_status}")

    # Draw visualization
    cv2.circle(frame, center, radius, (0, 0, 255), 3)
    cv2.putText(frame, f"Detected: {color_status}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("Color Detection Debug", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()