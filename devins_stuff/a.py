import cv2
import face_recognition
import numpy as np
import copy
import time

# import matplotlib.pyplot as plt
# f, ax = plt.subplots(1,2)

want_to_debug = True

video_capture = cv2.VideoCapture(0)

devin_image = face_recognition.load_image_file("devin_uner.png")
devin_face_encoding = face_recognition.face_encodings(devin_image)[0]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

backgrounds = []
background = None
result = None

first_frame = None
seen_first = False

box = None
has_one_box = False

seen_admin = False

start_time = time.time()

iterations = 0
last_seen_admin = None

last_five_with_admin = []

while True:
    iterations += 1
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    debug_frame = copy.deepcopy(frame)
    

    if not seen_first:
        seen_first = True
        first_frame = frame
        debug_frame = copy.deepcopy(frame)
    
    if len(backgrounds) < 5:
        backgrounds += [frame]
    elif len(backgrounds) == 5:
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

    # this sucks fix it l8r if possible
    f = open("invis.txt", "r")
    txt = ""
    for line in f:
        txt += line
    f.close()
    wants_invisable = "1" in txt
    if wants_invisable or want_to_debug:
            
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame[:, :, ::-1]

        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        # print(face_locations)
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            face_comp = face_recognition.compare_faces([devin_face_encoding], face_encoding)
            if True in face_comp:
                # admin is in frame
                seen_admin = True
                location_of_face = face_locations[face_comp.index(True)]
                last_seen_admin = location_of_face
                top, right, bottom, left = location_of_face
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                
                

                # now detect their body

                
                h, w, c = frame.shape
                
                
                

                # fill a box around the face
                cv2.rectangle(dilation, (left, top), (right, bottom), (255, 255, 255), -1)


               


                

                center = ((left+right)/2.0,(top+bottom)/2.0)
            if False in face_comp and last_seen_admin != None:

                for face in face_locations:

                    # detect if other face is in front of last known admin face
                    admin_top, admin_right, admin_bottom, admin_left = last_seen_admin
                    top, right, bottom, left = face

                    center_admin = ((admin_left+admin_right)/2.0,(admin_top+admin_bottom)/2.0)
                    center = ((left+right)/2.0,(top+bottom)/2.0)

                    if abs(center_admin[0]-center[0]) + abs(center_admin[1] - center[1]) < 200 and (bottom - top)*(right - left) > (admin_bottom - admin_top)*(admin_right - admin_left) and len(last_five_with_admin) >= 5:
                        print("SITUATION!!!")

                        
                        nether_background = last_five_with_admin[0]
                        nether_background = cv2.addWeighted(nether_background, 0.2**(1/8.0), last_five_with_admin[1], 0.2**(1/8.0), 0)
                        nether_background = cv2.addWeighted(nether_background, 0.2**(1/8.0), last_five_with_admin[2], 0.2**(1/4.0), 0)
                        nether_background = cv2.addWeighted(nether_background, 0.2**(1/4.0), last_five_with_admin[3], 0.2**(1/2.0), 0)
                        nether_background = cv2.addWeighted(nether_background, 0.2**(1/2.0), last_five_with_admin[4], 0.2,          0)

                        netherless_background = frame - nether_background

                        # ret, thresh = cv2.threshold(less_background, 127, 255, 0)
                        netherimgray = cv2.cvtColor(netherless_background,cv2.COLOR_BGR2GRAY)
                        thresh, netherless_background = cv2.threshold(netherimgray, 100, 255, cv2.THRESH_BINARY)
                        kernel = np.ones((5,5),np.uint8)
                        dilation = cv2.dilate(netherless_background,kernel,iterations = 1)

                        _, contours_of_front_person, _ = cv2.findContours(front_person_frame_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        print(contours_of_front_person)
                        target_contours_of_front_person = [x for x in contours if cv2.contourArea(x) > 10000 and cv2.contourArea(x) < 500000 and cv2.pointPolygonTest(x,center,True) > 0]

                        print(target_contours_of_front_person)
                        cv2.drawContours(front_person_frame_dilated, target_contours_of_front_person, -1, (0,0,255), 3)


        if seen_admin:
            last_five_with_admin += [frame]
            if len(last_five_with_admin) > 5:
                last_five_with_admin = last_seen_admin[1:]

            # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            _, contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            target_contours = [x for x in contours if cv2.contourArea(x) > 10000 and cv2.contourArea(x) < 500000 and cv2.pointPolygonTest(x,center,True) > 0]

            
            # cv2.drawContours(debug_frame, target_contours, -1, (0,255,0), 3)
            

            if len(target_contours) > 0:
                found_box = cv2.boundingRect(target_contours[0])

                if not has_one_box and found_box[2]+found_box[3] < 1500:
                    box = found_box
                    has_one_box = True
                if has_one_box and abs(found_box[2]-box[2]) < 600 and abs(found_box[3]-box[3]) < 400 and found_box[2]+found_box[3] < 1500:
                    box = found_box
                elif not has_one_box or top < box[0] or bottom > box[0]+box[2] or left < box[1] or right > box[1]+box[3]:
                    box = found_box
                    print("somethings wrong but we are ignoring it because otherwise the user would appear")
            



        # print(box)
        if box != None:

            if want_to_debug:
                # for debugging...
                cv2.rectangle(debug_frame, (int(box[0]),int(box[1]-100)), (int(box[0])+int(box[2]),int(int(box[1])+box[3])), (0,0,255),5)

            if wants_invisable:
                # fill the countor
                # cv2.rectangle(frame, (int(box[0]),int(box[1])), (int(box[0])+int(box[2]),int(int(box[1])+box[3])), (0,0,0),10)
                cv2.rectangle(frame, (int(box[0]-150),int(box[1]-100)), (int(box[0])+int(box[2])+150,int(int(box[1])+box[3])), (0,0,0),-1)
                # # cv2.fillPoly(frame, pts =boxes[0], color=(0,0,0))
                
                # fill everything in old one with black
                stencil = np.zeros(first_frame.shape).astype(first_frame.dtype)
                # fill the stencil with white in the box
                cv2.rectangle(stencil, (int(box[0]-150),int(box[1]-100)), (int(box[0])+int(box[2])+150,int(int(box[1])+box[3])), (255,255,255),-1)
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
        cv2.imshow('Video', front_person_frame_dilated)
        # cv2.imshow('Video 2', cv2.resize(np.hstack((blurred, debug_frame)), (0,0), fx=0.5, fy=0.5))
        print(iterations / (time.time() - start_time))
    except Exception as e:
        print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break