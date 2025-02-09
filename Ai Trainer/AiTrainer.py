import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("curl.mp4")
detector = pm.poseDetector()

count = 0
dir = 0
pTime = 0

while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    frame = detector.findPose(frame, False)
    lmList = detector.findPosition(frame, False)

    if len(lmList) != 0:
        angle = detector.findAngle(frame, 12, 14, 16)
        per = np.interp(angle, (40, 160), (100, 0))  # 40° -> %100, 160° -> %0
        bar = np.interp(angle, (40, 160), (650, 100))

        color = (255, 0, 255)
        if angle <= 90:
            color = (0, 255, 0)
            if dir == 0:
                count += 1
                dir = 1
        elif angle >= 160:
            color = (0, 255, 0)
            if dir == 1:
                dir = 0


        cv2.putText(frame, str(int(count)), (1150, 150), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)
        cv2.putText(frame, f'Angle: {int(angle)}', (50, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)


    cv2.imshow("CURL COUNTER", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
