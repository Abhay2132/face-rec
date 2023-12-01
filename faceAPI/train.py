import mainAPI
import pickle
import os
from pathlib import Path

def read():
    with Path(os.path.join("output", "encodings.pkl")).open(mode="rb") as f:
        loaded_encodings = pickle.load(f)
        print(loaded_encodings)

print("Training on Images")
mainAPI.SavedEncoding.trainModel("hog")
read()
