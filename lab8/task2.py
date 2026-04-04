import cv2

REF_POINT = cv2.imread('ref-point.jpg')
THRESHOLD = 135

capture = cv2.VideoCapture(0)
active_scene = None
view_mode = 5  # 1-обычное, 2-ч/б, 3-ч/б с размытием, 4-бинарное, 5-контуры

while True:
    ret, frame = capture.read()
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