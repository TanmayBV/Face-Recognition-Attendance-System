import mysql.connector
import numpy as np
import pickle
import face_recognition_api
from sklearn.preprocessing import LabelEncoder
import io
from PIL import Image

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="face_attendance"
    )

# Fetch images and photo IDs from the 'photos' table
def fetch_images_from_db():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT photo_id, photo FROM photos")
    records = cursor.fetchall()
    cursor.close()
    db.close()
    return records

# Encode images and store encodings back in MySQL
def create_and_save_encodings():
    db = connect_db()
    cursor = db.cursor()

    records = fetch_images_from_db()
    encodings = []
    labels = []

    for record in records:
        photo_id, image_data = record
        
        # Convert BLOB data to an image array
        image = Image.open(io.BytesIO(image_data))
        img = np.array(image)
        
        # Generate face encodings
        face_encodings = face_recognition_api.face_encodings(img)

        if len(face_encodings) > 1:
            print(f'More than one face found for photo ID {photo_id}. Only considering the first face.')
        elif len(face_encodings) == 0:
            print(f'No face found for photo ID {photo_id}. Skipping.')
            continue

        encoding = face_encodings[0]
        encodings.append(encoding)
        labels.append(photo_id)

        # Convert encoding to a comma-separated string
        encoding_str = ",".join([str(val) for val in encoding])
        
        # Save encoding to MySQL in the 'photos' table
        cursor.execute(
            "UPDATE photos SET encoding = %s WHERE photo_id = %s",
            (encoding_str, photo_id)
        )
        print(f'Encoded and saved for photo ID {photo_id} successfully.')

    db.commit()
    cursor.close()
    db.close()

    # Optionally save label encoding info to a file
    le = LabelEncoder().fit(labels)
    with open("labels.pkl", "wb") as f:
        pickle.dump(le, f)
    print("Labels saved to labels.pkl")

# Main function
if __name__ == "__main__":
    create_and_save_encodings()
