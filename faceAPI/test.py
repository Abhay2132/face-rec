import pickle
from pathlib import Path
import mainAPI
import os

cwd = os.sep.join(__file__.split(os.sep)[:-1])
img_path = (os.path.join(cwd, 'validation', "unknown", "group.jpg"))
output_loc = (os.path.join(cwd, "validation", "labeled", "group_labeled.jpg"))


def identify():
    e = mainAPI.SavedEncoding.encodings
    frame = mainAPI.FaceAPI.loadImage(img_path)
    persons, face_locations = mainAPI.FaceAPI.identify(frame, e)

    print(persons)
    mainAPI.FaceAPI.drawBox(frame, face_locations, persons)
    mainAPI.FaceAPI.saveImage(output_loc, frame)
    # _frame.save(output_loc)

    return 0


mainAPI.FaceAPI.init()
mainAPI.SavedEncoding.trainModel()


# print(main.SavedEncoding.encodings)

def read():
    with Path(os.path.join("output", "encodings.pkl")).open(mode="rb") as f:
        loaded_encodings = pickle.load(f)
        print("encodings : ", loaded_encodings)


read()
identify()
