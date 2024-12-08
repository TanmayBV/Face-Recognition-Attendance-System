import mysql.connector
import mysql.connector
import pickle
import numpy as np
from sklearn import neighbors
from sklearn.preprocessing import LabelEncoder

# Database connection details
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="face_attendance"
    )

# Fetch encoded data and labels (names) from the server
def fetch_encoded_data():
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT employee_id, name, encoding FROM photos WHERE encoding IS NOT NULL")
    records = cursor.fetchall()
    
    encodings = []
    labels = []
    
    for record in records:
        emp_id, name, encoding_str = record
        # Convert encoding string back to a numpy array
        encoding = np.array([float(val) for val in encoding_str.split(",")])
        encodings.append(encoding)
        labels.append(name)  # Store employee name instead of ID
    
    cursor.close()
    db.close()
    
    return np.array(encodings), np.array(labels)

# Train KNN classifier and save in (LabelEncoder, classifier) tuple format
def train_classifier(X, y):
    le = LabelEncoder().fit(y)
    y_encoded = le.transform(y)
    
    clf = neighbors.KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree', weights='distance')
    clf.fit(X, y_encoded)
    
    # Save the model in tuple format: (LabelEncoder, classifier)
    model_data = (le, clf)
    with open("classifier.pkl", "wb") as f:
        pickle.dump(model_data, f)
    
    return model_data

# Save the trained model back to the server
def save_model_to_server():
    db = connect_db()
    cursor = db.cursor()
    
    # Save the model as a BLOB in the database
    with open("classifier.pkl", "rb") as f:
        binary_model = f.read()
    
    # Store the model in the 'model' table (adjust table and field names as needed)
    cursor.execute("REPLACE INTO model (model_data) VALUES (%s)", (binary_model,))
    
    db.commit()
    cursor.close()
    db.close()

# Main function
def run():
    # Fetch encoded data from server
    X, y = fetch_encoded_data()
    
    # Train classifier and save in (LabelEncoder, classifier) tuple format
    train_classifier(X, y)
    
    # Save the model back to the server
    save_model_to_server()
    
    print('\x1b[6;30;42m' + "Classifier trained and saved to the server successfully." + '\x1b[0m')
