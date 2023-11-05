from pathlib import Path
import main
import os

cwd = os.sep.join(__file__.split(os.sep)[:-1])
img_path = (os.path.join(cwd, 'validation', "unknown", "group.jpg"))
output_loc = (os.path.join(cwd, "validation", "labeled", "group_labeled.jpg"))

def train():
    tdir = Path(os.path.join(cwd,"training"))
    print(tdir)

    for filepath in tdir.glob("*/*"):

        dirname = filepath.parent.name.split("_")
        image = main.FaceAPI.loadImage(filepath)
        
        name = "_".join(dirname[:-1])
        id= dirname[-1]

        main.FaceAPI.addPerson(image, name, id)
    
def identify():
    e = main.SavedEncoding.encodings
    _frame, persons = main.FaceAPI.identify(main.FaceAPI.loadImage(img_path), e)

    print(persons, output_loc)

    main.FaceAPI.saveImage(output_loc, _frame)
    # _frame.save(output_loc)

    return 0


main.FaceAPI.init()
# train()
# print(main.SavedEncoding.encodings)
identify()