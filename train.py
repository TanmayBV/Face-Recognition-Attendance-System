import mysql.connector
import pickle
import numpy as np
from sklearn import neighbors
from sklearn.preprocessing import LabelEncoder
import io

# Database connection details
def connect_db():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12743844",
        password="ZDezf3Y1Xn",
        database="sql12743844"
    )

# Fetch encoded data and labels from the server
def fetch_encoded_data():
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT employee_id, encoding FROM photos WHERE encoding IS NOT NULL")
    records = cursor.fetchall()
    
    encodings = []
    labels = []
    
    for record in records:
        emp_id, encoding_str = record
        # Convert encoding string back to a numpy array
        encoding = np.array([float(val) for val in encoding_str.split(",")])
        encodings.append(encoding)
        labels.append(emp_id)
    
    cursor.close()
    db.close()
    
    return np.array(encodings), np.array(labels)

# Train KNN classifier
def train_classifier(X, y):
    le = LabelEncoder().fit(y)
    y_encoded = le.transform(y)
    
    clf = neighbors.KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree', weights='distance')
    clf.fit(X, y_encoded)
    
    # Save LabelEncoder and classifier to file
    model_data = {'label_encoder': le, 'classifier': clf}
    with open("classifier.pkl", "wb") as f:
        pickle.dump(model_data, f)
    
    return model_data

# Save the trained model back to the server
def save_model_to_server(model_data):
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
if __name__ == "__main__":
    # Fetch encoded data from server
    X, y = fetch_encoded_data()
    
    # Train classifier
    model_data = train_classifier(X, y)
    
    # Save the model back to the server
    save_model_to_server(model_data)
    
    print('\x1b[6;30;42m' + "Classifier trained and saved to the server successfully." + '\x1b[0m')
