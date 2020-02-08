import numpy as np
import cv2

capture = cv2.VideoCapture('evan.mp4')
old_frame = None

frames = []


while True:
    ret, frame = capture.read()

    if ret:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if(len(frames) < 10):
            frames.append(frame)
        else :
            frames = np.array(frames)
            mean = np.mean(frames)
            diff = frame - mean
            print(mean)
            diff -= diff.min()
            disp = np.uint(255.0*diff/float(diff.max()))
            cv2.imshow('diff', disp)
        old_frame = gray

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        print('ERROR!')
        break

cap.release()
cv2.destroyAllWindows()     