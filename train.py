import os
import pickle
import numpy as np
import pandas as pd
from sklearn import neighbors
from sklearn.preprocessing import LabelEncoder

encoding_file_path = './encoded-images-data.csv'
labels_fName = 'labels.pkl'

if os.path.isfile(encoding_file_path):
    df = pd.read_csv(encoding_file_path)
else:
    print('\x1b[0;37;41m' + '{} does not exist'.format(encoding_file_path) + '\x1b[0m')
    quit()

if os.path.isfile(labels_fName):
    with open(labels_fName, 'rb') as f:
        le = pickle.load(f)
else:
    print('\x1b[0;37;41m' + '{} does not exist'.format(labels_fName) + '\x1b[0m')
    quit()

full_data = np.array(df.astype(float).values.tolist())
X = np.array(full_data[:, 1:-1])
y = np.array(full_data[:, -1])

clf = neighbors.KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree', weights='distance')
clf.fit(X, y.ravel())

fName = "./classifier.pkl"
backup_fName = "{}.bak".format(fName)

if os.path.isfile(backup_fName):
    os.remove(backup_fName)

if os.path.isfile(fName):
    print('\x1b[0;37;43m' + "{} already exists. Backing up.".format(fName) + '\x1b[0m')
    os.rename(fName, backup_fName)

with open(fName, 'wb') as f:
    pickle.dump((le, clf), f)
print('\x1b[6;30;42m' + "Saving classifier to '{}'".format(fName) + '\x1b[0m')
