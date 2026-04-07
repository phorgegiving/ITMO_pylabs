import cv2
import numpy as np

REF_POINT = cv2.imread('ref-point.jpg')
REF_GRAY = cv2.cvtColor(REF_POINT, cv2.COLOR_BGR2GRAY)
THRESHOLD = 135
RECOGNITION_THRESHOLD = 0.5

last_side = None
current_side = None
left_count = 0
right_count = 0

capture = cv2.VideoCapture(0)
ret, frame = capture.read()

_, cam_w, _ = frame.shape

active_scene = None
view_mode = 6  # 1-default, 2-b/w, 3-b/w with blur, 4-binary, 5-contours, 6-tracking

while True:
    ret, frame = capture.read()
    if not ret: break

    center_x, center_y = None, None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 1)
    _, binary_image = cv2.threshold(blur, THRESHOLD, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image=binary_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    if view_mode == 1:
        display = frame
    elif view_mode == 2:
        display = gray
    elif view_mode == 3:
        display = blur
    elif view_mode == 4:
        display = binary_image
    elif view_mode == 5:
        display = frame.copy()
        cv2.drawContours(image=display, contours=contours, contourIdx=-1, 
                        color=(0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
    elif view_mode == 6:
        display = frame.copy()
        result = cv2.matchTemplate(gray, REF_GRAY, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= RECOGNITION_THRESHOLD:
            h, w = REF_GRAY.shape

            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2

            cv2.rectangle(display, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            cv2.circle(display, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.circle(display, (center_x, center_y), w//2, (255, 0, 0), 1)

            coord_text = f"Center: ({center_x}, {center_y})"
            cv2.putText(display, coord_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)

            if center_x <= cam_w // 2:
                current_side = "L"
            else:
                current_side = "R"
            if current_side != last_side:
                last_side = current_side
                if current_side == "L":
                    left_count += 1
                else:
                    right_count += 1

            cv2.putText(display, f"Current Position: {current_side}", (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(display, "Reference point not found", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(display, f"Last Position: {last_side}", (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(display, f"Counts: L: {left_count}, R: {right_count}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow('cam capture', display)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("attempting to exit")
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