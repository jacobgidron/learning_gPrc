import cv2

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    frame[::7,::,::] = 55
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord('q'):
        # print(frame.shape)
        # print(frame.dtype)
        break
cap.release()
