import cv2
import face_recognition
import numpy as np


video_capture = cv2.VideoCapture(0)

devin_image = face_recognition.load_image_file("devin_uner.png")
devin_face_encoding = face_recognition.face_encodings(devin_image)[0]

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        if True in face_recognition.compare_faces([devin_face_encoding], face_encoding):
            # admin is in frame
            location_of_face = face_locations[face_recognition.compare_faces([devin_face_encoding], face_encoding).index(True)]

            top, right, bottom, left = location_of_face
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            center = ((left+right)/2.0,(top+bottom)/2.0)
            

            # now detect their body
            # edges = cv2.Canny(frame,100,200)

            # draw a line at the bottom of the screen
            h, w, c = frame.shape
            # cv2.rectangle(frame, (50, h-5), (w-50, h), (0, 0, 0), 10)

            imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = [x for x in contours if cv2.contourArea(x) > 1000 and cv2.pointPolygonTest(x,center,True) > 0]




            cv2.drawContours(frame, contours, -1, (0,255,0), 3)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


        

    try:
        cv2.imshow('Video', frame)
    except Exception as e:
        print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break