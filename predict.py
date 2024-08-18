import os
import pickle
import numpy as np
import pandas as pd
import face_recognition_api  # Assuming this is your custom module

def get_prediction_images(prediction_dir):
    files = [x[2] for x in os.walk(prediction_dir)]
    if len(files) == 0 or len(files[0]) == 0:
        print(f"No image files found in the directory: {prediction_dir}")
        return []
    
    exts = [".jpg", ".jpeg", ".png"]
    image_files = []
    for file in files[0]:
        _, ext = os.path.splitext(file)
        if ext.lower() in exts:
            image_files.append(os.path.join(prediction_dir, file))
    
    return image_files

def get_image_name_from_path(path):
    return os.path.basename(path)

fname = 'classifier.pkl'
prediction_dir = './test-images'
encoding_file_path = './encoded-images-data.csv'

# Load encodings
df = pd.read_csv(encoding_file_path)
full_data = np.array(df.astype(float).values.tolist())

# Extract features and labels
X = np.array(full_data[:, 1:-1])
y = np.array(full_data[:, -1])

# Load the classifier and label encoder
if os.path.isfile(fname):
    with open(fname, 'rb') as f:
        try:
            (le, clf) = pickle.load(f)
        except Exception as e:
            print("Error loading pickle file:", e)
            quit()
else:
    print('\x1b[0;37;43m' + "Classifier '{}' does not exist".format(fname) + '\x1b[0m')
    quit()

# Get image paths for prediction
image_paths = get_prediction_images(prediction_dir)

if not image_paths:
    print("No images to process. Exiting.")
    quit()

for image_path in image_paths:
    print('\x1b[6;30;42m' + "===== Predicting faces in '{}' =====".format(image_path) + '\x1b[0m')

    img = face_recognition_api.load_image_file(image_path)
    X_faces_loc = face_recognition_api.face_locations(img)
    faces_encodings = face_recognition_api.face_encodings(img, known_face_locations=X_faces_loc)
    print("Found {} faces in the image".format(len(faces_encodings)))

    if len(faces_encodings) > 0:
        # Adjust the number of features if necessary
        face_encodings = [encoding[:clf.n_features_in_] for encoding in faces_encodings]

        # Ensure n_neighbors does not exceed the number of samples the classifier was trained with
        n_neighbors = min(len(faces_encodings), clf.n_samples_fit_)

        # Use kneighbors with the dynamically determined n_neighbors
        closest_distances = clf.kneighbors(face_encodings, n_neighbors=n_neighbors)
        
        # Increase the threshold for recognizing faces if necessary
        threshold = 0.5
        is_recognized = [closest_distances[0][i][0] <= threshold for i in range(len(X_faces_loc))]

        predictions = [(le.inverse_transform([int(pred)])[0].title(), loc) if rec else (get_image_name_from_path(image_path), loc) 
                       for pred, loc, rec in zip(clf.predict(face_encodings), X_faces_loc, is_recognized)]

        for i, (name, loc) in enumerate(predictions):
            # Print detailed information for debugging
            distance = closest_distances[0][i][0] if i < len(closest_distances[0]) else 'N/A'
            print(f"Prediction: {name} at location {loc} with distance {distance}")
    else:
        print("No faces found to predict.")

    print()
