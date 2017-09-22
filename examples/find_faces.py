import face_recognition
from pymongo import MongoClient
import cv2



client = MongoClient("mongodb://bellbot:Hero30888899@54.94.185.144:27017/bellbot")
db = client.bellbot
cursor = db.person.find({"face_encoding": {"$exists" : "true"}},{"name":1, "face_encoding":1})
count = 0

names = []
mongo_face_encoding = []
for document in cursor:
    names.append(document['name'])
    mongo_face_encoding.append(document['face_encoding'])

video_capture = cv2.VideoCapture(0)

process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations,num_jitters=10)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matchs = face_recognition.compare_faces(mongo_face_encoding, face_encoding, 0.5)
            name = "Unknown"

            count = 0
            for match in matchs:
                if match:
                    name = names[count]
                count += 1

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()









