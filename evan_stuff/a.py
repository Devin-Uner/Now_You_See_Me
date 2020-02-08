import cv2

video_capture = cv2.VideoCapture('evan.mp4')


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    try:
    	cv2.imshow('Video', frame)
    except Exception as e:
    	print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
