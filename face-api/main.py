from pathlib import Path
from PIL import ImageTk
import pickle
import face_recognition
import cv2
import os
import numpy as np
import threading

cwd = os.sep.join(__file__.split(os.sep)[:-1])
DEFAULT_ENCODINGS_PATH = Path(os.path.join(cwd,"output/encodings.pkl"))

class SavedEncoding :
    encodings = {"persons" : [], "encodings":[]}
    # { person : [(person_id, person_name)]  , encodings : [NDArray] }

    @staticmethod
    def loadEncoding(encodings_location : Path = DEFAULT_ENCODINGS_PATH):
        with encodings_location.open(mode="rb") as f:
            SavedEncoding.saved_encodings = pickle.load(f)

    @staticmethod
    def saveEncoding(output_loc:Path=DEFAULT_ENCODINGS_PATH):
        with output_loc.open(mode="wb") as f:
            pickle.dump(SavedEncoding.encodings, f)

    @staticmethod
    def addEncoding(encoding, name=False):
        if(not name):
           return
        persons = SavedEncoding.encodings["persons"]
        persons.append((len(persons), name))
        SavedEncoding.encodings["encodings"].append(encoding)

class FaceAPI: 

    @staticmethod
    def identify(frame, savedEncoding=SavedEncoding.encodings):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        persons = []
        for face_encoding in face_encodings :
            matches = face_recognition.compare_faces(SavedEncoding.encodings["encodings"], face_encoding)
            person = (-1, "unknown")

            face_distances = face_recognition.face_distance(savedEncoding, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                person = savedEncoding.persons[best_match_index]

            persons.append(person)

        for (top, right, bottom, left), person in zip(face_locations, persons):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            id, name = person
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name[1], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        return (frame, persons)

    
    @staticmethod
    def addPerson(image, name, pid=-1):
        face_encoding = face_recognition.face_encodings(image)
        for encoding in face_encoding:
            SavedEncoding.addEncoding(name, encoding, pid)
        SavedEncoding.saveEncoding()
