import os
import pickle
import face_recognition_api
import mysql.connector
import cv2
from datetime import datetime
import numpy as np

# Function to load the classifier and label encoder
def load_classifier():
    fname = 'classifier.pkl'
    if os.path.isfile(fname):
        with open(fname, 'rb') as f:
            data = pickle.load(f)
            if isinstance(data, tuple) and len(data) == 2:
                return data  # Label encoder and classifier
            else:
                raise ValueError("Unexpected classifier data format.")
    else:
        raise FileNotFoundError("Classifier file does not exist.")

# Function to connect to the database
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="face_attendance"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        quit()

# Fetch employee data from the database
def fetch_employee_data(cursor):
    cursor.execute("SELECT employee_id, employee_name FROM employee_attendance")
    return cursor.fetchall()

# Save attendance to the database
def save_attendance(cursor, db, employee_id, employee_name):
    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT attendance_dates FROM employee_attendance WHERE employee_id = %s", (employee_id,))
    result = cursor.fetchone()

    already_marked = False
    if result:
        attendance_dates = result[0] if result[0] else ""
        attendance_dates = attendance_dates.split(',')
        if current_date not in attendance_dates:
            attendance_dates.append(current_date)
            attendance_dates_str = ','.join(attendance_dates)
            cursor.execute(
                "UPDATE employee_attendance SET attendance_dates = %s WHERE employee_id = %s",
                (attendance_dates_str, employee_id)
            )
            db.commit()
            print(f"Attendance updated for {employee_name}")
        else:
            print(f"Attendance already recorded for {employee_name} today.")
            already_marked = True
    else:
        cursor.execute(
            "INSERT INTO employee_attendance (employee_id, name, attendance_dates) VALUES (%s, %s, %s)",
            (employee_id, employee_name, current_date)
        )
        db.commit()
        print(f"Attendance recorded for {employee_name}.")
    return already_marked

# Process video frames for face recognition
def process_video(le, clf, db, cursor):
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_processing_interval = 2  # Process every 2nd frame
    frame_count = 0

    # Persistent results
    persistent_face_locations = []
    persistent_face_names = []
    persistent_face_colors = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        frame_count += 1

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        if frame_count % frame_processing_interval == 0:
            # Detect faces and encode
            persistent_face_locations = face_recognition_api.face_locations(small_frame)
            face_encodings = face_recognition_api.face_encodings(small_frame, persistent_face_locations)

            # Reset face names and colors
            persistent_face_names = []
            persistent_face_colors = []

            if len(face_encodings) > 0:
                closest_distances = clf.kneighbors(face_encodings, n_neighbors=1)
                is_recognized = [closest_distances[0][i][0] <= 0.5 for i in range(len(persistent_face_locations))]

                for pred, loc, rec in zip(clf.predict(face_encodings), persistent_face_locations, is_recognized):
                    name = le.inverse_transform([int(pred)])[0] if rec else "Unknown"
                    persistent_face_names.append(name)

                    if name != "Unknown":
                        employee_data = fetch_employee_data(cursor)
                        already_marked = False
                        for emp_id, emp_name in employee_data:
                            if str(emp_name) == str(name):
                                already_marked = save_attendance(cursor, db, emp_id, emp_name)
                                persistent_face_colors.append((0, 255, 0) if already_marked else (0, 0, 255))
                                break
                    else:
                        persistent_face_colors.append((0, 0, 255))

        # Display the results on the original frame
        for (name, (top, right, bottom, left)), color in zip(zip(persistent_face_names, persistent_face_locations), persistent_face_colors):
            # Scale back up the face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Display name or "Unknown" below the rectangle
            cv2.putText(frame, str(name), (left + 6, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Hit 'q' to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Main function
def run():
    # Load the classifier and label encoder
    try:
        le, clf = load_classifier()
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return

    # Connect to the database
    db = connect_db()
    cursor = db.cursor()

    try:
        # Process video frames for face recognition
        process_video(le, clf, db, cursor)
    finally:
        cursor.close()
        db.close()
