from pathlib import Path
from PIL import ImageTk
import pickle
import face_recognition
import cv2
import os

cwd = os.sep.join(__file__.split(os.sep)[:-1])
DEFAULT_ENCODINGS_PATH = Path(os.path.join(cwd,"output/encodings.pkl"))

class FR: # Face Recognisor

    saved_encodings = []

    @staticmethod
    def identify(frame):
        face_ids = []

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings :
            matches = face_recognition.compare_faces(SavedEncoding.encodings["encodings"], face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
        return     
    
    @staticmethod
    def loadEncoding(encodings_location : Path = DEFAULT_ENCODINGS_PATH):
        with encodings_location.open(mode="rb") as f:
            FR.saved_encodings = pickle.load(f)

class SavedEncoding :
    encodings = []

    @staticmethod
    def loadEncoding():
        return 0

    def saveEncoding():
        return 0

    def addEncoding(name, encoding):
        SavedEncoding.encodings["names"].append(name)
        SavedEncoding.encodings["encodings"].append(encoding)
