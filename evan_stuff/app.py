import cv2
import face_recognition

video_capture = cv2.VideoCapture('evan.mp4')

devin_image = face_recognition.load_image_file("evan.jpg")
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

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


        

    try:
        cv2.imshow('Video', frame)
    except Exception as e:
        print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break