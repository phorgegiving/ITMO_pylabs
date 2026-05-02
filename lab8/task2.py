import cv2
import numpy as np

REF_POINT = cv2.imread('lab8/ref-point.jpg')
REF_GRAY = cv2.cvtColor(REF_POINT, cv2.COLOR_BGR2GRAY)
THRESHOLD = 135
RECOGNITION_THRESHOLD = 0.5
FLY_IMAGE = cv2.imread('lab8/fly64.png', cv2.IMREAD_UNCHANGED)


def overlay_image_centered(base, overlay, x, y):
    h, w = overlay.shape[:2]
    y1, x1 = y - h // 2, x - w // 2
    base[y1 : y1 + h, x1 : x1 + w] = overlay[:, :, :3]

last_side = None
left_count = 0
right_count = 0

capture = cv2.VideoCapture(0)
ret, frame = capture.read()

cam_w = frame.shape[1]
view_mode = 6

while True:
    ret, frame = capture.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    _, binary_image = cv2.threshold(blur, THRESHOLD, 255, cv2.THRESH_BINARY)

    if view_mode == 1:
        display = frame
    elif view_mode == 2:
        display = gray
    elif view_mode == 3:
        display = blur
    elif view_mode == 4:
        display = binary_image
    elif view_mode == 5:
        display = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
    else:
        display = frame.copy()
        result = cv2.matchTemplate(gray, REF_GRAY, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= RECOGNITION_THRESHOLD:
            h, w = REF_GRAY.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2

            cv2.rectangle(display, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            cv2.circle(display, (center_x, center_y), 5, (0, 0, 255), -1)
            overlay_image_centered(display, FLY_IMAGE, center_x, center_y)

            current_side = "L" if center_x <= cam_w // 2 else "R"
            if current_side != last_side:
                last_side = current_side
                if current_side == "L":
                    left_count += 1
                else:
                    right_count += 1

            cv2.putText(display, f"Center: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display, f"Current Position: {current_side}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(display, "Reference point not found", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(display, f"Last Position: {last_side}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(display, f"Counts: L: {left_count}, R: {right_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('cam capture', display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('1'):
        view_mode = 1
    elif key == ord('2'):
        view_mode = 2
    elif key == ord('3'):
        view_mode = 3
    elif key == ord('4'):
        view_mode = 4
    elif key == ord('5'):
        view_mode = 5

capture.release()
cv2.destroyAllWindows()