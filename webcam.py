import cv2
import os
import dlib
import numpy as np
import pickle
import pandas as pd
from datetime import datetime, timedelta

# Load the trained classifier and label encoder
with open('classifier.pkl', 'rb') as f:
    le, clf = pickle.load(f)

# Load Dlib models for face detection and face recognition
face_detector = dlib.get_frontal_face_detector()
predictor_model = './models/shape_predictor_68_face_landmarks.dat'
pose_predictor = dlib.shape_predictor(predictor_model)
face_recognition_model = './models/dlib_face_recognition_resnet_model_v1.dat'
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

# Initialize attendance DataFrame
excel_file_path = 'attendance.xlsx'
if os.path.isfile(excel_file_path):
    df = pd.read_excel(excel_file_path)
else:
    df = pd.DataFrame(columns=['Name', 'Timestamp'])

last_attendance_time = {}

def save_attendance(name):
    global df
    current_time = datetime.now()

    if name in last_attendance_time:
        last_time = last_attendance_time[name]
        if current_time - last_time < timedelta(hours=1):
            return
    
    new_entry = pd.DataFrame({'Name': [name], 'Timestamp': [current_time]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_excel(excel_file_path, index=False)
    last_attendance_time[name] = current_time

def generate_frames():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_detector(rgb_small_frame)
        face_encodings = []
        for face_location in face_locations:
            shape = pose_predictor(rgb_small_frame, face_location)
            face_encodings.append(np.array(face_encoder.compute_face_descriptor(rgb_small_frame, shape)))

        predictions = []

        if len(face_encodings) > 0:
            face_encodings = [encoding[:clf.n_features_in_] for encoding in face_encodings]
            closest_distances = clf.kneighbors(face_encodings, n_neighbors=1)
            is_recognized = [closest_distances[0][i][0] <= 0.5 for i in range(len(face_locations))]
            predictions = [(le.inverse_transform([int(pred)])[0].title(), loc) if rec else ("Unknown", loc)
                           for pred, loc, rec in zip(clf.predict(face_encodings), face_locations, is_recognized)]

            for name, _ in predictions:
                if name != "Unknown":
                    save_attendance(name)

        for name, rect in predictions:
            top, right, bottom, left = rect.top(), rect.right(), rect.bottom(), rect.left()
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video_capture.release()
