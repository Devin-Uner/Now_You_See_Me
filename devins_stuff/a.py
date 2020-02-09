import cv2
import face_recognition
import numpy as np
import copy

video_capture = cv2.VideoCapture(0)

devin_image = face_recognition.load_image_file("devin_uner.png")
devin_face_encoding = face_recognition.face_encodings(devin_image)[0]
evan_image = face_recognition.load_image_file("Evan_Mills.jpg")
evan_face_encoding = face_recognition.face_encodings(evan_image)[0]

names = ["devin", "evan"]
encodings = [devin_face_encoding, evan_face_encoding]



backgrounds = []
background = None
result = None

first_frame = None
seen_first = False

box = [None, None]
has_one_box = [False, False]

seen_admin = False

iteration = 0

while True:
    iteration += 1
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    data_frame = copy.deepcopy(frame)

    if not seen_first:
        seen_first = True
        first_frame = frame
        


    

    if len(backgrounds) < 5:
        backgrounds += [frame]
    if len(backgrounds) == 5:
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

    f = open("invis.txt", "r")
    txt = ""
    for line in f:
        txt += line
    f.close()
    if "1" in txt and len(backgrounds) >= 5:
            
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame[:, :, ::-1]

        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for i, face_encoding in enumerate(face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(encodings, face_encoding)
            print(matches, face_locations)
            if True in matches:
                # admin is in frame
                seen_admin = True


                location_of_face = face_locations[i]
                index_of_face = matches.index(True)
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

                # cv2.rectangle(dilation, (50, h-2), (w-50, h-1), (0, 0, 0), 10)
                # cv2.rectangle(dilation, (50, h-1), (w-50, h), (255, 255, 255), 10)
                
                

                center = ((left+right)/2.0,(top+bottom)/2.0)

                # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
                _, contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                target_contours = [x for x in contours if cv2.contourArea(x) > 10000 and cv2.contourArea(x) < 500000 and cv2.pointPolygonTest(x,center,True) > 0]

                
                cv2.drawContours(data_frame, target_contours, -1, (0,255,0), 3)
                

                if len(target_contours) > 0:
                    found_box = cv2.boundingRect(target_contours[0])

                    if not has_one_box[index_of_face] and found_box[2]+found_box[3] < 1500:
                        box[index_of_face] = found_box
                        has_one_box[index_of_face] = True
                    if has_one_box[index_of_face] and abs(found_box[2]-box[index_of_face][2]) < 200 and abs(found_box[3]-box[index_of_face][3]) < 100 and found_box[2]+found_box[3] < 1500:
                        box[index_of_face] = found_box
                    elif not has_one_box[index_of_face] or top < box[index_of_face][0] or bottom > box[index_of_face][0]+box[index_of_face][2] or left < box[index_of_face][1] or right > box[index_of_face][1]+box[index_of_face][3]:
                        box[index_of_face] = found_box
                        print("somethings wrong but we are ignoring it because otherwise the user would appear")
           


        print(box)

        
        # cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[0]+box[2]), int(box[1]+box[3])), (0,0,255), 2)
        if box[0] != None or box[1] != None:
            for i, bo in enumerate(box):
                if bo != None and txt[i] == "1":
                    # for debugging...
                    cv2.rectangle(data_frame, (int(bo[0]),int(bo[1]-100)), (int(bo[0])+int(bo[2]),int(int(bo[1])+bo[3])), (0,0,255),5)

            # fill the countor
            # cv2.rectangle(frame, (int(box[0]),int(box[1])), (int(box[0])+int(box[2]),int(int(box[1])+box[3])), (0,0,0),10)
            for i, bo in enumerate(box):
                if bo != None and txt[i] == "1":
                    cv2.rectangle(frame, (int(bo[0]-150),int(bo[1]-100)), (int(bo[0])+int(bo[2])+150,int(int(bo[1])+bo[3])), (0,0,0),-1)
            # # cv2.fillPoly(frame, pts =boxes[0], color=(0,0,0))
            # cv2.imshow('Video3', frame)
            # fill everything in old one with black
            stencil = np.zeros(first_frame.shape).astype(first_frame.dtype)
            # fill the stencil with white in the box

            for i, bo in enumerate(box):
                if bo != None and txt[i] == "1":
                    cv2.rectangle(stencil, (int(bo[0]-150),int(bo[1]-100)), (int(bo[0])+int(bo[2])+150,int(int(bo[1])+bo[3])), (255,255,255),-1)
            # combined the stencil and the first frame to get just the part we want to paste in
            result = cv2.bitwise_and(first_frame, stencil)
            # cv2.imshow('Video2', result)
            # cv2.rectangle(frame, (int(boxes[0][0]),int(boxes[0][1])), (int(boxes[0][0])+int(boxes[0][2]),int(int(boxes[0][1])+boxes[0][3])), (0,0,255),3)
            frame = cv2.bitwise_or(result, frame)
            # cv2.imshow('Video', frame)
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