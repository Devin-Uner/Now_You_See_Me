import cv2
import face_recognition
import numpy as np
import copy
import time

video_capture = cv2.VideoCapture(0)
devin_face_encoding = face_recognition.face_encodings(face_recognition.load_image_file("devin_uner.png"))[0]


backgrounds = []
background = None
result = None

first_frame = None
seen_first = False

box = None
has_one_box = False

seen_admin = False

iteration = 0

calibration_boxes = [
    [0,0,200,200],
    [200,200,200,200],
    [400,400,200,200],
    [600,600,200,200],
    [700,700,200,200],
    [800,800,200,200],
]

calibration_index = 0

while True:
    iteration += 1
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    data_frame = copy.deepcopy(frame)

    if not seen_first:
        seen_first = True
        first_frame = frame
        data_frame = copy.deepcopy(frame)

    if len(backgrounds) < 5:
        backgrounds += [frame]
    if len(backgrounds) == 5:
        background = backgrounds[0]
        background = cv2.addWeighted(background, 0.2**(1/8.0), backgrounds[1], 0.2**(1/8.0), 0)
        background = cv2.addWeighted(background, 0.2**(1/8.0), backgrounds[2], 0.2**(1/4.0), 0)
        background = cv2.addWeighted(background, 0.2**(1/4.0), backgrounds[3], 0.2**(1/2.0), 0)
        background = cv2.addWeighted(background, 0.2**(1/2.0), backgrounds[4], 0.2,          10)

        less_background = frame - background

        hsv = cv2.cvtColor(less_background, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        v[v > 0] += 1
        v[v <= 0] = 0

        final_hsv = cv2.merge((h, s, v))

        less_background = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)


        # ret, thresh = cv2.threshold(less_background, 127, 255, 0)
        imgray = cv2.cvtColor(less_background,cv2.COLOR_BGR2GRAY)
        thresh, less_background = cv2.threshold(imgray, 100, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(less_background,kernel,iterations = 1)



    f = open("invis.txt", "r")
    txt = ""
    for line in f:
        txt += line
    f.close()
    if "1" in txt:  
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame[:, :, ::-1]

        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces([devin_face_encoding], face_encoding)
            if True in matches:
                # admin is in frame
                seen_admin = True
                location_of_face = face_locations[matches.index(True)]

                top, right, bottom, left = location_of_face
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                
                

                # now detect their body
                # edges = cv2.Canny(frame,100,200)

                
                h, w, c = frame.shape
                
                # fill a box around the face
                cv2.rectangle(dilation, (left, top), (right, bottom), (255, 255, 255), -1)

                # # blur = cv2.GaussianBlur(frame,(7,7),0)
                # # blur = cv2.blur(frame,(14,14))
                # imgray = cv2.cvtColor(less_background,cv2.COLOR_BGR2GRAY)
                

                # # draw a line at the bottom of the screen
                cv2.rectangle(dilation, (50, h-20), (w-50, h-10), (0, 0, 0), 10)
                cv2.rectangle(dilation, (50, h-10), (w-50, h), (255, 255, 255), 10)


                

                center = ((left+right)/2.0,(top+bottom)/2.0)

        if seen_admin:
            # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            _, contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            target_contours = [x for x in contours if cv2.contourArea(x) > 10000 and cv2.contourArea(x) < 500000 and cv2.pointPolygonTest(x,center,True) > 0]

            
            cv2.drawContours(data_frame, target_contours, -1, (0,255,0), 3)
            

            if len(target_contours) > 0:
                found_box = cv2.boundingRect(target_contours[0])
                if found_box[2]*found_box[3] > 2500 and found_box[2]*found_box[3] < 600000:
                    box = found_box
                cv2.rectangle(data_frame, (int(found_box[0]),int(found_box[1]-100)), (int(found_box[0])+int(found_box[2]),int(int(found_box[1])+found_box[3])), (255,0,0),5)
                print(found_box[2]*found_box[3])
                # if not has_one_box and found_box[2]+found_box[3] < 1000:
                #     box = found_box
                #     has_one_box = True
                # if has_one_box and ((abs(found_box[2]-box[2]) < 200 and abs(found_box[3]-box[3]) < 100)) and found_box[2]+found_box[3] < 1000:
                #     box = found_box
                # elif not has_one_box or top < box[0] or bottom > box[0]+box[2] or left < box[1] or right > box[1]+box[3]:
                #     box = found_box
                #     print("somethings wrong but we are ignoring it because otherwise the user would appear")

           

        if calibration_index < len(calibration_boxes):
            box = calibration_boxes[calibration_index]
            print("calibrating with:", box)
            calibration_index += 1
            if calibration_index == len(calibration_boxes):
                box = None
        print(box)
        if box != None:
            # cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[0]+box[2]), int(box[1]+box[3])), (0,0,255), 2)
            
            # for debugging...
            cv2.rectangle(data_frame, (int(box[0]),int(box[1]-100)), (int(box[0])+int(box[2]),int(int(box[1])+box[3])), (0,0,255),5)

            # fill the countor
            # cv2.rectangle(frame, (int(box[0]),int(box[1])), (int(box[0])+int(box[2]),int(int(box[1])+box[3])), (0,0,0),10)
            cv2.rectangle(frame, (int(box[0]-150),int(box[1]-100)), (int(box[0])+int(box[2])+150,int(int(box[1])+box[3]+100)), (0,0,0),-1)
            # # cv2.fillPoly(frame, pts =boxes[0], color=(0,0,0))
            
            # fill everything in old one with black
            stencil = np.zeros(first_frame.shape).astype(first_frame.dtype)
            # fill the stencil with white in the box
            cv2.rectangle(stencil, (int(box[0]-150),int(box[1]-100)), (int(box[0])+int(box[2])+150,int(int(box[1])+box[3]+100)), (255,255,255),-1)
            # combined the stencil and the first frame to get just the part we want to paste in
            result = cv2.bitwise_and(first_frame, stencil)

            # cv2.rectangle(frame, (int(boxes[0][0]),int(boxes[0][1])), (int(boxes[0][0])+int(boxes[0][2]),int(int(boxes[0][1])+boxes[0][3])), (0,0,255),3)
            frame = cv2.bitwise_or(result, frame)

            first_frame = copy.deepcopy(frame)

            



    dst = np.empty_like(frame)
    noise = cv2.randn(dst, (0,0,0), (40,40,40))
    frame_noise = cv2.addWeighted(frame, 0.5, noise, 0.5, 30)
    # noise = cv2.randn(dst, (0,0,0), (20,20,20))
    # frame_noise = cv2.addWeighted(frame_noise, 0.5, noise, 0.5, 30)
    # noise = cv2.randn(dst, (0,0,0), (20,20,20))
    # frame_noise = cv2.addWeighted(frame_noise, 0.5, noise, 0.5, 30)

    blurred = cv2.GaussianBlur(frame_noise,(7,7),0)

        

    try:
        # cv2.imshow('Video', blurred)
        cv2.imshow('Video 2', cv2.resize(np.hstack((blurred, data_frame)), (0,0), fx=0.5, fy=0.5))
    except Exception as e:
        print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break