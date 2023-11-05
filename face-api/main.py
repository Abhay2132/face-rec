from pathlib import Path
from PIL import ImageTk, ImageDraw, Image
import pickle
import face_recognition
import cv2
import numpy as np
import os

cwd = os.sep.join(__file__.split(os.sep)[:-1])
DEFAULT_ENCODINGS_PATH = Path(os.path.join(cwd,"output/encodings.pkl"))

Path(os.path.join(cwd,"training")).mkdir(exist_ok=True)
Path(os.path.join(cwd,"output")).mkdir(exist_ok=True)
Path(os.path.join(cwd,"validation")).mkdir(exist_ok=True)

class SavedEncoding :
    encodings = {"persons" : [], "encodings":[]}
    # { person : [(person_id, person_name)]  , encodings : [NDArray] }

    @staticmethod
    def loadEncoding(encodings_location : Path = DEFAULT_ENCODINGS_PATH):
        if not os.path.isfile(encodings_location) :
            return
        with encodings_location.open(mode="rb") as f:
            SavedEncoding.encodings = pickle.load(f)

    @staticmethod
    def saveEncoding(output_loc:Path=DEFAULT_ENCODINGS_PATH):
        with output_loc.open(mode="wb") as f:
            pickle.dump(SavedEncoding.encodings, f)

    @staticmethod
    def addEncoding(encoding, name:str, pid):
        SavedEncoding.encodings["persons"].append((pid, name))
        SavedEncoding.encodings["encodings"].append(encoding)

    @staticmethod
    def getEncodings():
        return SavedEncoding.encodings

class FaceAPI: 

    @staticmethod
    def init():
        SavedEncoding.loadEncoding()

    @staticmethod
    def identify(frame, savedEncoding = SavedEncoding.getEncodings()):
        rgb_small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        persons = []
        known_face_encoding = savedEncoding["encodings"]
        # print(f"known_face_encoding : {known_face_encoding}")
        for face_encoding in face_encodings :
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            person = (-1, "unknown")

            face_distances = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                person = savedEncoding["persons"][best_match_index]

            persons.append(person)

        # pillow_image = Image.fromarray(frame)
        # draw = ImageDraw.Draw(pillow_image)

        for (top, right, bottom, left), person in zip(face_locations, persons):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            id, name = person

            # clr = name == "unknown" if "red" else "green"
            # draw.rectangle(((left, top), (right, bottom)), outline=clr)
            # text_left, text_top, text_right, text_bottom = draw.textbbox((left, bottom), name)
            # draw.rectangle(
            #     ((text_left, text_top), (text_right, text_bottom)),
            #     fill=clr,
            #     outline=clr,
            # )
            # draw.text(
            #     (text_left, text_top),
            #     name,
            #     fill="white",
            # )

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # del draw
        return (frame, persons)

    @staticmethod
    def saveImage(dest , image):
        cv2.imwrite(dest, image)

    
    @staticmethod
    def addPerson(image, name, pid=-1):
        face_encoding = face_recognition.face_encodings(image)
        for encoding in face_encoding:
            SavedEncoding.addEncoding(encoding, name, pid)
        SavedEncoding.saveEncoding()

    @staticmethod
    def loadImage(imagePath:str):
        return cv2.imread(imagePath)
        # return face_recognition.load_image_file(imagePath)