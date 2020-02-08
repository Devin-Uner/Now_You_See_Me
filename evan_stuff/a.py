import cv2
import face_recognition
import numpy as np


video_capture = cv2.VideoCapture(0)

devin_image = face_recognition.load_image_file("devin_uner.png")
devin_face_encoding = face_recognition.face_encodings(devin_image)[0]
fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

backgrounds = []
background = None
result = None

first_frame = None
seen_first = False

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if not seen_first:
        seen_first = True
        first_frame = frame
        hsv = cv2.cvtColor(first_frame, cv2.COLOR_BGR2HSV)
        hsv[:,:,2] += 20
        first_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    blur = cv2.GaussianBlur(frame,(7,7),0)
    blur = cv2.blur(frame,(14,14))

    if len(backgrounds) < 5:
        backgrounds += [frame]
    else:
        background = backgrounds[0]
        background = cv2.addWeighted(background, 0.2**(1/8.0), backgrounds[1], 0.2**(1/8.0), 0)
        background = cv2.addWeighted(background, 0.2**(1/8.0), backgrounds[2], 0.2**(1/4.0), 0)
        background = cv2.addWeighted(background, 0.2**(1/4.0), backgrounds[3], 0.2**(1/2.0), 0)
        background = cv2.addWeighted(background, 0.2**(1/2.0), backgrounds[4], 0.2,          0)

        less_background = frame - background

        # ret, thresh = cv2.threshold(less_background, 127, 255, 0)
        imgray = cv2.cvtColor(less_background,cv2.COLOR_BGR2GRAY)
        thresh, less_background = cv2.threshold(imgray, 100, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(less_background,kernel,iterations = 1)

        
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
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
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            
            

            # now detect their body
            # edges = cv2.Canny(frame,100,200)

            
            h, w, c = frame.shape
            
            
            # fgmask = fgbg.apply(frame)
            # frame = cv2.bitwise_or(frame,frame,mask = fgmask)
            # frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

            # fill a box around the face
            cv2.rectangle(dilation, (left, top), (right, bottom), (255, 255, 255), -1)

            less_background = cv2.bitwise_or(frame,frame,mask = dilation)

            # blur = cv2.GaussianBlur(frame,(7,7),0)
            # blur = cv2.blur(frame,(14,14))
            imgray = cv2.cvtColor(less_background,cv2.COLOR_BGR2GRAY)

            # draw a line at the bottom of the screen
            cv2.rectangle(imgray, (50, h-20), (w-50, h-10), (0, 0, 0), 10)
            cv2.rectangle(imgray, (50, h-10), (w-50, h), (255, 255, 255), 10)


            

            center = ((left+right)/2.0,(top+bottom)/2.0)

            # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = [x for x in contours if cv2.contourArea(x) > 1000 and cv2.contourArea(x) < 500000 and cv2.pointPolygonTest(x,center,True) > 0]




            # cv2.drawContours(frame, contours, -1, (0,255,0), 3)
            

            # fill the countor
            cv2.fillPoly(frame, pts =contours, color=(0,0,0))
            
            # fill everything in old one with black
            stencil = np.zeros(first_frame.shape).astype(first_frame.dtype)
            cv2.fillPoly(stencil, contours, [255,255,255])
            result = cv2.bitwise_and(first_frame, stencil)

            frame = cv2.bitwise_or(result, frame)


        

    try:
        cv2.imshow('Video', frame)
    except Exception as e:
        print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break