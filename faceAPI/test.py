from pathlib import Path
import mainAPI
import os

cwd = os.sep.join(__file__.split(os.sep)[:-1])
img_path = (os.path.join(cwd, 'validation', "unknown", "group.jpg"))
output_loc = (os.path.join(cwd, "validation", "labeled", "group_labeled.jpg"))


def train():
    tdir = Path(os.path.join(cwd, "training"))
    print(tdir)

    for filepath in tdir.glob("*/*"):
        dirname = filepath.parent.name.split("_")
        image = mainAPI.FaceAPI.loadImage(filepath)

        name = "_".join(dirname[:-1])
        id = dirname[-1]

        mainAPI.FaceAPI.addPerson(image, name, id)


def identify():
    e = mainAPI.SavedEncoding.encodings
    frame = mainAPI.FaceAPI.loadImage(img_path)
    persons, face_locations = mainAPI.FaceAPI.identify(frame, e)

    print(persons, output_loc)
    mainAPI.FaceAPI.drawBox(frame, face_locations, persons)
    mainAPI.FaceAPI.saveImage(output_loc, frame)
    # _frame.save(output_loc)

    return 0


mainAPI.FaceAPI.init()
# train()
# print(main.SavedEncoding.encodings)
identify()
