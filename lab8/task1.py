import cv2

img = cv2.imread('6.png')
scretched_img = cv2.resize(img, (512, 512), interpolation = cv2.INTER_LINEAR)

cv2.imshow("new", scretched_img)
cv2.imshow("old", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


#TODO: 2-3 задания это грубо говоря одно задание
#отслеживание с модификациями, вообще интересно
