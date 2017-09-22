import face_recognition
from pymongo import MongoClient
from urllib.request import urlopen

client = MongoClient("mongodb://bellbot:Hero30888899@54.94.185.144:27017/bellbot")
db = client.bellbot
cursor = db.person.find()
count = 0
for document in cursor:
    print("start load image")
    picture = urlopen(document['image'])
    image = face_recognition.load_image_file(picture)
    print("image loaded")
    print("start process")
    encodings = face_recognition.face_encodings(image, num_jitters = 50)
    print("finished process")
    if len(encodings) > 0:
        face_encoding = encodings[0]
        result = db.person.update_one(
            {"_id": document['_id']},
            {
                "$set": {
                    "face_encoding": face_encoding.tolist()
                },
                "$currentDate": {"lastModified": True}
            }
        )
        print(document['_id'])
    else:
        print("No faces found in the image!")
        print(document['_id'])
    print(count)
    count += 1








