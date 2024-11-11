import os
import pickle
import face_recognition_api
import mysql.connector
import cv2
from datetime import datetime
import numpy as np

# Load the classifier and label encoder from the pickle file
fname = 'classifier.pkl'
if os.path.isfile(fname):
    with open(fname, 'rb') as f:
        data = pickle.load(f)
        if isinstance(data, tuple) and len(data) == 2:
            le, clf = data  # Label encoder and classifier
        else:
            print("Unexpected classifier data format.")
            quit()
else:
    print("Classifier file does not exist.")
    quit()

# Function to connect to the database
def connect_db():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12743844",
        password="ZDezf3Y1Xn",
        database="sql12743844"
    )

# Fetch employee data from the database
def fetch_employee_data():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT employee_id, name FROM employee_attendance")
    records = cursor.fetchall()
    cursor.close()
    db.close()
    return records

# Save employee attendance
def save_attendance(employee_id, employee_name):
    db = connect_db()
    cursor = db.cursor()

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Check if the employee already has an attendance record for today
    cursor.execute("SELECT attendance_date FROM employee_attendance WHERE employee_id = %s", (employee_id,))
    result = cursor.fetchone()

    if result:
        attendance_dates = result[0].split(',')
        if current_date not in attendance_dates:
            attendance_dates.append(current_date)
            attendance_dates_str = ','.join(attendance_dates)
            cursor.execute("UPDATE employee_attendance SET attendance_date = %s WHERE employee_id = %s", 
                           (attendance_dates_str, employee_id))
            print(f"Attendance updated for {employee_name}")
        else:
            print(f"Attendance already recorded for {employee_name} today.")
    else:
        cursor.execute("INSERT INTO employee_attendance (employee_id, name, attendance_date) VALUES (%s, %s, %s)",
                       (employee_id, employee_name, current_date))
        print(f"Attendance recorded for {employee_name}.")

    db.commit()
    cursor.close()
    db.close()

# Initialize webcam for face recognition
video_capture = cv2.VideoCapture(0)

# Process video frames
while True:
    ret, frame = video_capture.read()

    # Resize frame to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Find all faces and face encodings in the frame
    face_locations = face_recognition_api.face_locations(small_frame)
    face_encodings = face_recognition_api.face_encodings(small_frame, face_locations)

    face_names = []
    if len(face_encodings) > 0:
        # Use KNN classifier to predict the label (ID) for the face
        closest_distances = clf.kneighbors(face_encodings, n_neighbors=1)

        is_recognized = [closest_distances[0][i][0] <= 0.5 for i in range(len(face_locations))]

        for pred, loc, rec, dist in zip(clf.predict(face_encodings), face_locations, is_recognized, closest_distances[0]):
            name = le.inverse_transform([int(pred)])[0] if rec else "Unknown"
            face_names.append(name)
            
            if name != "Unknown":
                # Fetch employee data and save attendance
                employee_data = fetch_employee_data()
                
                # Match the predicted ID with employee data
                for emp_id, emp_name in employee_data:
                    if str(emp_name) == str(name):  # Compare with the predicted name (as string)
                        save_attendance(emp_id, emp_name)

    # Display the results
    for name, (top, right, bottom, left) in zip(face_names, face_locations):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Display name or "Unknown" below the rectangle
        cv2.putText(frame, str(name), (left + 6, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
video_capture.release()
cv2.destroyAllWindows()
