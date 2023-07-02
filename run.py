import pandas as pd
import cv2
import urllib.request
import numpy as np
import os
import time
from firebase_admin import messaging
from datetime import datetime
import face_recognition
from google.cloud import storage
import firebase_admin
from firebase_admin import *
from google.cloud import storage
from google.oauth2.service_account import Credentials
cred = credentials.Certificate("firebase*.json")


firebase_admin.initialize_app(cred)

# Initialize the GCS client
client = storage.Client()
bucket = client.bucket('firebase*.com')

path = 'image_folder'
url = 'http://192.168.*.*/cam-lo.jpg'

# if 'Attendance.csv' in os.listdir(os.path.join(os.getcwd(), 'attendace')):
#     print("there iss..")
#     os.remove("Attendance.csv")
# else:
#     df = pd.DataFrame(list())
#     df.to_csv("Attendance.csv")

images = []
classNames = []
blobs = bucket.list_blobs(prefix=path)
for blob in blobs:
    blob_name = blob.name
    if blob_name.endswith('.jpg') or blob_name.endswith('.jpeg') or blob_name.endswith('.png'):
        blob_data = blob.download_as_bytes()
        nparr = np.frombuffer(blob_data, np.uint8)
        curImg = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        images.append(curImg)
        classNames.append(os.path.splitext(os.path.basename(blob_name))[0])

print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open("Attendance.csv", 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
def send_notification(name):
    message = messaging.Message(
        notification=messaging.Notification(
            title='Unknown person detected',
            body=f'{name} is an unknown person',
        ),
        topic='unknown_person_notification'
    )
    response = messaging.send(message)
    print('Notification sent:', response)

encodeListKnown = findEncodings(images)
print('Encoding Complete')

while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
        else:
            name = "Unknown"
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # Save the unknown person's photo to Firebase storage
            now = datetime.datetime.now()
            dtString = now.strftime('%Y%m%d-%H%M%S')
            filename = f"unknown-{dtString}.jpg"
            #bucket = storage.bucket("face-b9a67")
            blob = bucket.blob(filename)
            _, img_encoded = cv2.imencode('.jpg', img[y1:y2, x1:x2])
            blob.upload_from_string(img_encoded.tobytes(), content_type='image/jpeg')
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
            send_notification(name)
            
    cv2.imshow('Webcam', img)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
cv2.destroyAllWindows()
cv2.imread        
