import os
import pickle

fname = 'classifier.pkl'

if os.path.isfile(fname):
    with open(fname, 'rb') as f:
        try:
            data = pickle.load(f)
            print(f"Loaded data: {data}")
            print(f"Number of items: {len(data)}")
            if isinstance(data, tuple) and len(data) == 2:
                le, clf = data
                print("Label Encoder and Classifier loaded successfully.")
            else:
                print("Unexpected format. Data structure:", type(data))
        except Exception as e:
            print("Error loading pickle file:", e)
else:
    print(f"File '{fname}' does not exist.")
