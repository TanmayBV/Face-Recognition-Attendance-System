import face_recognition_api
import cv2
import os
import pickle
import numpy as np
import warnings

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load Face Recognizer classifier
fname = 'classifier.pkl'
if os.path.isfile(fname):
    with open(fname, 'rb') as f:
        try:
            le, clf = pickle.load(f)
        except Exception as e:
            print("Error loading pickle file:", e)
            quit()
else:
    print('\x1b[0;37;43m' + f"Classifier '{fname}' does not exist" + '\x1b[0m')
    quit()

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Ensure n_neighbors does not exceed the number of samples the classifier was trained with
n_neighbors = min(1, clf.n_samples_fit_)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to grab frame. Exiting.")
            break

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition_api.face_locations(small_frame)
            face_encodings = face_recognition_api.face_encodings(small_frame, face_locations)

            face_names = []
            predictions = []
            if len(face_encodings) > 0:
                # Adjust the number of features if necessary
                face_encodings = [encoding[:clf.n_features_in_] for encoding in face_encodings]

                # Use kneighbors with the dynamically determined n_neighbors
                closest_distances = clf.kneighbors(face_encodings, n_neighbors=n_neighbors)
                is_recognized = [closest_distances[0][i][0] <= 0.5 for i in range(len(face_locations))]

                predictions = [(le.inverse_transform([int(pred)])[0].title(), loc) if rec else ("Unknown", loc) 
                               for pred, loc, rec in zip(clf.predict(face_encodings), face_locations, is_recognized)]

        process_this_frame = not process_this_frame

        # Display the results
        for name, (top, right, bottom, left) in predictions:
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

        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam and close the window
video_capture.release()
cv2.destroyAllWindows()
